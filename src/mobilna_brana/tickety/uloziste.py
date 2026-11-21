# SDD: generované z specification 0.2.1 · contract API-Tickets 0.1.0 (approved) · baseline B-01 · prompt implement-change v1.0 · 2026-11-21
"""Uloženie DO-Ticket v databáze mobilnej brány (ART-DatabazaMobilnejBrany, ADR-004).

Okrem ticketov uchováva auditné záznamy zmien stavu (QR-002), idempotency kľúče (Q-11) a zlyhania notifikácií (QR-003).
Prechody stavu sú atómové – podmienka na aktuálny stav je súčasťou zápisu, takže pri súbehu uspeje iba prvý (BR-001).
"""

import sqlite3
import threading
from dataclasses import dataclass
from typing import Optional

_SCHEMA = """
CREATE TABLE IF NOT EXISTS ticket (
    id TEXT PRIMARY KEY,
    ziadatel_id TEXT NOT NULL,
    adresat_typ TEXT NOT NULL,
    vyucujuci_id TEXT,
    predmet TEXT NOT NULL,
    popis TEXT NOT NULL,
    stav TEXT NOT NULL,
    posudzovatel_id TEXT,
    odovodnenie TEXT,
    cas_podania TEXT NOT NULL,
    cas_zmeny_stavu TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_stavu (
    ticket_id TEXT NOT NULL,
    kto TEXT NOT NULL,
    kedy TEXT NOT NULL,
    z_stavu TEXT,
    do_stavu TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS idempotency (
    pouzivatel_id TEXT NOT NULL,
    kluc TEXT NOT NULL,
    otlacok_obsahu TEXT NOT NULL,
    ticket_id TEXT NOT NULL,
    PRIMARY KEY (pouzivatel_id, kluc)
);
CREATE TABLE IF NOT EXISTS zlyhanie_notifikacie (
    ticket_id TEXT NOT NULL,
    kedy TEXT NOT NULL,
    stav TEXT NOT NULL
);
"""


@dataclass
class TicketZaznam:
    id: str
    ziadatel_id: str
    adresat_typ: str
    vyucujuci_id: Optional[str]
    predmet: str
    popis: str
    stav: str
    posudzovatel_id: Optional[str]
    odovodnenie: Optional[str]
    cas_podania: str
    cas_zmeny_stavu: str


class Uloziste:
    def __init__(self, cesta: str = ":memory:") -> None:
        self._db = sqlite3.connect(cesta, check_same_thread=False, isolation_level=None)
        self._db.row_factory = sqlite3.Row
        self._zamok = threading.Lock()
        self._db.executescript(_SCHEMA)

    # --- čítanie -------------------------------------------------------------------------------
    def nacitaj(self, ticket_id: str) -> Optional[TicketZaznam]:
        with self._zamok:
            riadok = self._db.execute("SELECT * FROM ticket WHERE id = ?", (ticket_id,)).fetchone()
        return TicketZaznam(**dict(riadok)) if riadok else None

    def zoznam(self, sql_podmienka: str, parametre: tuple) -> list[TicketZaznam]:
        with self._zamok:
            riadky = self._db.execute(
                f"SELECT * FROM ticket WHERE {sql_podmienka} ORDER BY cas_podania", parametre
            ).fetchall()
        return [TicketZaznam(**dict(r)) for r in riadky]

    def audit(self, ticket_id: str) -> list[dict]:
        with self._zamok:
            riadky = self._db.execute(
                "SELECT * FROM audit_stavu WHERE ticket_id = ? ORDER BY rowid", (ticket_id,)
            ).fetchall()
        return [dict(r) for r in riadky]

    def zlyhania_notifikacii(self) -> list[dict]:
        with self._zamok:
            return [dict(r) for r in self._db.execute("SELECT * FROM zlyhanie_notifikacie").fetchall()]

    # --- zápis ---------------------------------------------------------------------------------
    def vytvor(self, t: TicketZaznam, kluc: str, otlacok: str) -> tuple[str, bool]:
        """Uloží ticket a idempotency kľúč v jednej transakcii.

        Vráti (ticket_id, nový). Ak kľúč už existuje, vráti pôvodný ticket a nový=False;
        rozdiel v obsahu rieši volajúci podľa vráteného otlačku (pozri otlacok_kluca).
        """
        with self._zamok:
            self._db.execute("BEGIN IMMEDIATE")
            try:
                existujuci = self._db.execute(
                    "SELECT ticket_id FROM idempotency WHERE pouzivatel_id = ? AND kluc = ?",
                    (t.ziadatel_id, kluc),
                ).fetchone()
                if existujuci:
                    self._db.execute("COMMIT")
                    return existujuci["ticket_id"], False
                self._db.execute(
                    "INSERT INTO ticket VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (t.id, t.ziadatel_id, t.adresat_typ, t.vyucujuci_id, t.predmet, t.popis, t.stav,
                     t.posudzovatel_id, t.odovodnenie, t.cas_podania, t.cas_zmeny_stavu),
                )
                self._db.execute(
                    "INSERT INTO idempotency VALUES (?,?,?,?)", (t.ziadatel_id, kluc, otlacok, t.id)
                )
                self._db.execute(
                    "INSERT INTO audit_stavu VALUES (?,?,?,?,?)",
                    (t.id, t.ziadatel_id, t.cas_podania, None, t.stav),
                )
                self._db.execute("COMMIT")
                return t.id, True
            except Exception:
                self._db.execute("ROLLBACK")
                raise

    def otlacok_kluca(self, pouzivatel_id: str, kluc: str) -> Optional[str]:
        with self._zamok:
            r = self._db.execute(
                "SELECT otlacok_obsahu FROM idempotency WHERE pouzivatel_id = ? AND kluc = ?",
                (pouzivatel_id, kluc),
            ).fetchone()
        return r["otlacok_obsahu"] if r else None

    def zmen_stav(
        self,
        ticket_id: str,
        z_stavu: str,
        do_stavu: str,
        kto: str,
        kedy: str,
        pozadovany_posudzovatel: Optional[str] = None,
        novy_posudzovatel: Optional[str] = None,
        odovodnenie: Optional[str] = None,
    ) -> bool:
        """Atómový prechod stavu s auditným záznamom. Vráti False, ak podmienka už neplatí (súbeh)."""
        podmienka = "id = ? AND stav = ?"
        parametre: list = [ticket_id, z_stavu]
        if pozadovany_posudzovatel is not None:
            podmienka += " AND posudzovatel_id = ?"
            parametre.append(pozadovany_posudzovatel)
        with self._zamok:
            self._db.execute("BEGIN IMMEDIATE")
            try:
                kurzor = self._db.execute(
                    f"""UPDATE ticket SET stav = ?, cas_zmeny_stavu = ?,
                           posudzovatel_id = COALESCE(?, posudzovatel_id),
                           odovodnenie = COALESCE(?, odovodnenie)
                        WHERE {podmienka}""",
                    [do_stavu, kedy, novy_posudzovatel, odovodnenie, *parametre],
                )
                if kurzor.rowcount != 1:
                    self._db.execute("ROLLBACK")
                    return False
                self._db.execute(
                    "INSERT INTO audit_stavu VALUES (?,?,?,?,?)", (ticket_id, kto, kedy, z_stavu, do_stavu)
                )
                self._db.execute("COMMIT")
                return True
            except Exception:
                self._db.execute("ROLLBACK")
                raise

    def zaznamenaj_zlyhanie_notifikacie(self, ticket_id: str, kedy: str, stav: str) -> None:
        with self._zamok:
            self._db.execute("INSERT INTO zlyhanie_notifikacie VALUES (?,?,?)", (ticket_id, kedy, stav))

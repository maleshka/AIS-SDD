# SDD: generované z specification 0.2.1 · contract API-Tickets 0.1.0 (approved) · baseline B-01 · prompt implement-change v1.0 · 2026-11-21
"""AS-SpravaTicketov realizovaná funkciou AF-EvidenciaTicketov v AC-MobilnaBrana (ADR-001).

Vynucuje pravidlá BR-001…BR-007 a lifecycle DO-Ticket (spec/application/lifecycles.yaml).
"""

import hashlib
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional

from ..identity import Pouzivatel, ROLA_STUDIJNE_ODDELENIE, ROLA_VYUCUJUCI
from ..notifikacie import OdosielatelNotifikacii
from .uloziste import TicketZaznam, Uloziste

log = logging.getLogger("mobilna_brana.tickety")

PODANY = "podany"
V_POSUDZOVANI = "v_posudzovani"
SCHVALENY = "schvaleny"
ZAMIETNUTY = "zamietnuty"
ROZHODNUTE = {SCHVALENY, ZAMIETNUTY}

ADRESAT_VYUCUJUCI = "vyucujuci"
ADRESAT_SO = "studijne_oddelenie"


@dataclass
class ProblemTicketu(Exception):
    """Porušené pravidlo – API ho preloží na application/problem+json."""

    status: int
    titulok: str
    pravidlo: Optional[str] = None
    detail: Optional[str] = None
    chybajuce_udaje: list[str] = field(default_factory=list)


def _teraz() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class SluzbaTicketov:
    def __init__(
        self,
        uloziste: Uloziste,
        odosielatel: OdosielatelNotifikacii,
        hodiny: Callable[[], str] = _teraz,
    ) -> None:
        self._u = uloziste
        self._notifikacie = odosielatel
        self._teraz = hodiny

    # --- viditeľnosť (BR-003) ------------------------------------------------------------------
    @staticmethod
    def _je_adresat(t: TicketZaznam, p: Pouzivatel) -> bool:
        """Adresát ticketu (Q-03): zvolený vyučujúci alebo ktorýkoľvek zamestnanec ŠO."""
        if t.adresat_typ == ADRESAT_VYUCUJUCI:
            return p.rola == ROLA_VYUCUJUCI and t.vyucujuci_id == p.id
        return p.rola == ROLA_STUDIJNE_ODDELENIE

    def _vidi(self, t: TicketZaznam, p: Pouzivatel) -> bool:
        return (p.je_ziadatel and t.ziadatel_id == p.id) or (p.je_posudzovatel and self._je_adresat(t, p))

    def _nacitaj_viditelny(self, ticket_id: str, p: Pouzivatel) -> TicketZaznam:
        t = self._u.nacitaj(ticket_id)
        if t is None or not self._vidi(t, p):
            # Cudzí ticket sa správa ako neexistujúci (BR-003, SC-002-04).
            raise ProblemTicketu(404, "Ticket neexistuje", pravidlo="BR-003")
        return t

    # --- operácie ------------------------------------------------------------------------------
    def podaj(self, p: Pouzivatel, kluc: str, predmet: str, popis: str, adresat_typ: str,
              vyucujuci_id: Optional[str]) -> tuple[TicketZaznam, bool]:
        """podatTicket – BP-VytvorenieTicketu, BR-005, Q-11."""
        if not p.je_ziadatel:
            raise ProblemTicketu(403, "Ticket môže podať iba študent", pravidlo="BR-002")
        obsah = json.dumps([predmet, popis, adresat_typ, vyucujuci_id], ensure_ascii=False)
        otlacok = hashlib.sha256(obsah.encode()).hexdigest()
        povodny_otlacok = self._u.otlacok_kluca(p.id, kluc)
        if povodny_otlacok is not None and povodny_otlacok != otlacok:
            raise ProblemTicketu(409, "Idempotency-Key bol použitý s iným obsahom", detail="Q-11")
        teraz = self._teraz()
        novy = TicketZaznam(
            id=str(uuid.uuid4()), ziadatel_id=p.id, adresat_typ=adresat_typ, vyucujuci_id=vyucujuci_id,
            predmet=predmet, popis=popis, stav=PODANY, posudzovatel_id=None, odovodnenie=None,
            cas_podania=teraz, cas_zmeny_stavu=teraz,
        )
        ticket_id, vytvoreny = self._u.vytvor(novy, kluc, otlacok)
        return self._u.nacitaj(ticket_id), vytvoreny

    def zoznam(self, p: Pouzivatel, stav: Optional[str]) -> list[TicketZaznam]:
        """zoznamTicketov – iba tickety viditeľné podľa BR-003."""
        if p.je_ziadatel:
            podmienka, parametre = "ziadatel_id = ?", [p.id]
        elif p.rola == ROLA_VYUCUJUCI:
            podmienka, parametre = "adresat_typ = ? AND vyucujuci_id = ?", [ADRESAT_VYUCUJUCI, p.id]
        elif p.rola == ROLA_STUDIJNE_ODDELENIE:
            podmienka, parametre = "adresat_typ = ?", [ADRESAT_SO]
        else:
            return []
        if stav is not None:
            podmienka += " AND stav = ?"
            parametre.append(stav)
        return self._u.zoznam(podmienka, tuple(parametre))

    def detail(self, p: Pouzivatel, ticket_id: str) -> TicketZaznam:
        """detailTicketu – BR-003."""
        return self._nacitaj_viditelny(ticket_id, p)

    def prevezmi(self, p: Pouzivatel, ticket_id: str) -> TicketZaznam:
        """prevziatTicket – podany → v_posudzovani (BR-002, BR-004, Q-19)."""
        t = self._nacitaj_viditelny(ticket_id, p)
        if not p.je_posudzovatel:
            raise ProblemTicketu(403, "Ticket môže prevziať iba posudzovateľ – jeho adresát", pravidlo="BR-002")
        if t.stav != PODANY:
            pravidlo = "BR-001" if t.stav in ROZHODNUTE else "BR-004"
            raise ProblemTicketu(409, "Ticket už nie je v stave Podaný", pravidlo=pravidlo)
        if not self._u.zmen_stav(t.id, PODANY, V_POSUDZOVANI, kto=p.id, kedy=self._teraz(), novy_posudzovatel=p.id):
            raise ProblemTicketu(409, "Ticket medzitým prevzal iný posudzovateľ", pravidlo="BR-004")
        return self._u.nacitaj(t.id)

    def rozhodni(self, p: Pouzivatel, ticket_id: str, vysledok: str, odovodnenie: Optional[str]) -> TicketZaznam:
        """rozhodnutTicket – v_posudzovani → schvaleny | zamietnuty (BR-001, BR-002, BR-004, BR-006, BR-007)."""
        t = self._nacitaj_viditelny(ticket_id, p)
        if not p.je_posudzovatel:
            raise ProblemTicketu(403, "O tickete nemôže rozhodnúť žiadateľ", pravidlo="BR-002")
        if t.stav in ROZHODNUTE:
            raise ProblemTicketu(409, "Ticket je už rozhodnutý", pravidlo="BR-001")
        if t.stav != V_POSUDZOVANI:
            raise ProblemTicketu(409, "Rozhodnúť možno iba prevzatý ticket", pravidlo="BR-004")
        if t.posudzovatel_id != p.id:
            raise ProblemTicketu(403, "Rozhodnúť môže iba posudzovateľ, ktorý ticket prevzal", pravidlo="BR-004")
        if vysledok == ZAMIETNUTY and not (odovodnenie and odovodnenie.strip()):
            raise ProblemTicketu(422, "Zamietnutie musí obsahovať odôvodnenie", pravidlo="BR-006",
                                 chybajuce_udaje=["odovodnenie"])
        if not self._u.zmen_stav(t.id, V_POSUDZOVANI, vysledok, kto=p.id, kedy=self._teraz(),
                                 pozadovany_posudzovatel=p.id, odovodnenie=odovodnenie):
            # Súbeh: iné rozhodnutie bolo zaznamenané skôr (BR-001).
            raise ProblemTicketu(409, "Ticket je už rozhodnutý", pravidlo="BR-001")
        self._oznam_vysledok(t.ziadatel_id, t.id, vysledok)
        return self._u.nacitaj(t.id)

    # --- BR-007, ADR-003 -----------------------------------------------------------------------
    def _oznam_vysledok(self, ziadatel_id: str, ticket_id: str, stav: str) -> None:
        """Notifikácia iba pri rozhodnutí; zlyhanie nemení rozhodnutie a zaznamená sa (QR-003).
        Log obsahuje iba identifikátor ticketu a stav (QR-004)."""
        try:
            self._notifikacie.odosli(ziadatel_id, ticket_id, stav)
        except Exception:
            self._u.zaznamenaj_zlyhanie_notifikacie(ticket_id, self._teraz(), stav)
            log.warning("Notifikáciu o tickete %s (stav %s) sa nepodarilo odoslať", ticket_id, stav)

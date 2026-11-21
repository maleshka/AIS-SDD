# SDD: generované z specification 0.2.1 · contract API-Tickets 0.1.0 (approved) · baseline B-01 · prompt implement-change v1.0 · 2026-11-21
"""AS-Notifikacie – oznámenie výsledku žiadateľovi (BP-OznamenieVysledku, INT-003, ADR-003).

Notifikácia obsahuje iba identifikátor ticketu a stav (QR-004). Doručenie zabezpečuje TS-NotifikacnaSluzba
(NODE-FCM); produkčný adaptér nie je súčasťou výrezu R-002.
"""

from typing import Protocol


class OdosielatelNotifikacii(Protocol):
    def odosli(self, prijemca_id: str, ticket_id: str, stav: str) -> None:
        """Odošle notifikáciu; pri zlyhaní vyhodí výnimku."""
        ...

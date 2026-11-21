# SDD: generované z specification 0.2.1 · contract API-Tickets 0.1.0 (approved) · baseline B-01 · prompt implement-change v1.0 · 2026-11-21
"""Identita prihláseného používateľa (QR-001, rozhodnutia Q-10a a Q-10b).

Identitu aj rolu dodáva existujúce prihlásenie aplikácie Moje štúdium. Produkčné napojenie nie je súčasťou
výrezu R-002; brána dostane implementáciu rozhrania OverovacIdentity zvonka.
"""

from dataclasses import dataclass
from typing import Optional, Protocol

ROLA_STUDENT = "student"
ROLA_VYUCUJUCI = "vyucujuci"
ROLA_STUDIJNE_ODDELENIE = "studijne_oddelenie"

ROLY_POSUDZOVATELA = {ROLA_VYUCUJUCI, ROLA_STUDIJNE_ODDELENIE}


@dataclass(frozen=True)
class Pouzivatel:
    id: str
    rola: str

    @property
    def je_ziadatel(self) -> bool:
        """ROLE-Ziadatel plní ACT-Student."""
        return self.rola == ROLA_STUDENT

    @property
    def je_posudzovatel(self) -> bool:
        """ROLE-Posudzovatel plní ACT-PedagogickyZbor alebo ACT-ZamestnanecSO."""
        return self.rola in ROLY_POSUDZOVATELA


class OverovacIdentity(Protocol):
    def over(self, token: str) -> Optional[Pouzivatel]:
        """Vráti používateľa pre platný bearer token, inak None."""
        ...

# SDD: demo spúšťač k specification 0.2.1 · contract API-Tickets 0.1.0 · baseline B-01
"""Ukážka API-Tickets v prehliadači – iba na predvedenie, nie produkčné nasadenie.

Spustenie:  .venv/bin/python demo.py   →  otvor http://127.0.0.1:8000/docs

Prihlásenie aj notifikačná služba sú nahradené ukážkovými verziami (rovnaké ako v testoch):
do poľa "authorization" pri operácii napíš napr.  Bearer t-student-1
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))

import uvicorn  # noqa: E402

from mobilna_brana.api import create_app
from mobilna_brana.identity import Pouzivatel, ROLA_STUDENT, ROLA_STUDIJNE_ODDELENIE, ROLA_VYUCUJUCI
from mobilna_brana.tickety.uloziste import Uloziste

POUZIVATELIA = {
    "t-student-1": Pouzivatel("stu-1", ROLA_STUDENT),
    "t-student-2": Pouzivatel("stu-2", ROLA_STUDENT),
    "t-vyucujuci-1": Pouzivatel("vyu-1", ROLA_VYUCUJUCI),
    "t-so-1": Pouzivatel("so-1", ROLA_STUDIJNE_ODDELENIE),
    "t-so-2": Pouzivatel("so-2", ROLA_STUDIJNE_ODDELENIE),
}


class DemoOverovac:
    def over(self, token):
        return POUZIVATELIA.get(token)


class DemoNotifikacie:
    def odosli(self, prijemca_id, ticket_id, stav):
        print(f"📱 NOTIFIKÁCIA pre {prijemca_id}: ticket {ticket_id} je teraz '{stav}'")


app = create_app(Uloziste(), DemoOverovac(), DemoNotifikacie())

if __name__ == "__main__":
    print("\nAPI-Tickets demo → http://127.0.0.1:8000/docs")
    print("Tokeny: " + ", ".join(f"Bearer {t}" for t in POUZIVATELIA) + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)

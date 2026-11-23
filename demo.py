# SDD: demo spúšťač k specification 0.2.1 · contract API-Tickets 0.1.0 · baseline B-01
"""Ukážka API-Tickets v prehliadači – iba na predvedenie, nie produkčné nasadenie.

Spustenie:  .venv/bin/python demo.py   →  otvor http://127.0.0.1:8000/  (webová ukážka)
                                       alebo http://127.0.0.1:8000/docs (Swagger)

Webová ukážka (demo_ui/index.html) volá iba operácie schváleného contractu. Cesty / a /demo/notifikacie
pridáva len tento spúšťač, nie sú súčasťou API-Tickets ani candidate code v src/.

Prihlásenie aj notifikačná služba sú nahradené ukážkovými verziami (rovnaké ako v testoch):
do poľa "authorization" pri operácii napíš napr.  Bearer t-student-1
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))

import uvicorn  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402

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


ODOSLANE_NOTIFIKACIE: list[dict] = []


class DemoNotifikacie:
    def odosli(self, prijemca_id, ticket_id, stav):
        print(f"📱 NOTIFIKÁCIA pre {prijemca_id}: ticket {ticket_id} je teraz '{stav}'")
        t = uloziste.nacitaj(ticket_id)
        ODOSLANE_NOTIFIKACIE.append(
            {"prijemca": prijemca_id, "ticketId": ticket_id, "stav": stav, "predmet": t.predmet if t else ticket_id}
        )


uloziste = Uloziste()
app = create_app(uloziste, DemoOverovac(), DemoNotifikacie())
UI = pathlib.Path(__file__).resolve().parent / "demo_ui" / "index.html"


@app.get("/", include_in_schema=False)
def ukazka():
    return FileResponse(UI)


@app.get("/demo/notifikacie", include_in_schema=False)
def notifikacie():
    return ODOSLANE_NOTIFIKACIE

if __name__ == "__main__":
    print("\nWebová ukážka → http://127.0.0.1:8000/")
    print("Swagger       → http://127.0.0.1:8000/docs")
    print("Tokeny: " + ", ".join(f"Bearer {t}" for t in POUZIVATELIA) + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)

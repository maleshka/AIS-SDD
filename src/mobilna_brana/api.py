# SDD: generované z specification 0.2.1 · contract API-Tickets 0.1.0 (approved) · baseline B-01 · prompt implement-change v1.0 · 2026-11-21
"""AIF-APIBrany – HTTP rozhranie API-Tickets 0.1.0 (spec/contracts/approved/api-tickets.openapi.yaml).

Contract sa tu nemení; všetky cesty, operationId, status kódy a tvary odpovedí zodpovedajú approved verzii.
"""

from typing import Annotated, Literal, Optional

from fastapi import Depends, FastAPI, Header, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .identity import OverovacIdentity, Pouzivatel
from .notifikacie import OdosielatelNotifikacii
from .tickety.sluzba import ProblemTicketu, SluzbaTicketov
from .tickety.uloziste import TicketZaznam, Uloziste

PROBLEM = "application/problem+json"
StavTicketu = Literal["podany", "v_posudzovani", "schvaleny", "zamietnuty"]


# --- schémy podľa components.schemas ----------------------------------------------------------
class Adresat(BaseModel):
    model_config = ConfigDict(extra="forbid")
    typ: Literal["vyucujuci", "studijne_oddelenie"]
    vyucujuciId: Optional[str] = None

    @model_validator(mode="after")
    def _kontrola(self) -> "Adresat":
        if self.typ == "vyucujuci" and not self.vyucujuciId:
            raise ValueError("vyucujuciId je povinné pre adresáta typu vyucujuci")
        if self.typ == "studijne_oddelenie" and self.vyucujuciId is not None:
            raise ValueError("vyucujuciId sa pri adresátovi studijne_oddelenie neuvádza")
        return self


class NovyTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    predmet: str = Field(min_length=1, max_length=200)
    popis: str = Field(min_length=1, max_length=5000)
    adresat: Adresat


class Rozhodnutie(BaseModel):
    model_config = ConfigDict(extra="forbid")
    vysledok: Literal["schvaleny", "zamietnuty"]
    odovodnenie: Optional[str] = Field(default=None, min_length=1, max_length=2000)


def _ticket_json(t: TicketZaznam) -> dict:
    adresat = {"typ": t.adresat_typ}
    if t.vyucujuci_id is not None:
        adresat["vyucujuciId"] = t.vyucujuci_id
    return {
        "id": t.id, "predmet": t.predmet, "popis": t.popis, "adresat": adresat, "stav": t.stav,
        "ziadatelId": t.ziadatel_id, "posudzovatelId": t.posudzovatel_id, "odovodnenie": t.odovodnenie,
        "casPodania": t.cas_podania, "casZmenyStavu": t.cas_zmeny_stavu,
    }


def _problem(status: int, titulok: str, pravidlo: Optional[str] = None, detail: Optional[str] = None,
             chybajuce: Optional[list[str]] = None) -> JSONResponse:
    telo: dict = {"type": "about:blank", "title": titulok, "status": status}
    if detail:
        telo["detail"] = detail
    if pravidlo:
        telo["pravidlo"] = pravidlo
    if chybajuce:
        telo["chybajuceUdaje"] = chybajuce
    return JSONResponse(telo, status_code=status, media_type=PROBLEM)


class _Neprihlaseny(Exception):
    pass


def create_app(uloziste: Uloziste, overovac: OverovacIdentity, odosielatel: OdosielatelNotifikacii) -> FastAPI:
    app = FastAPI(title="API-Tickets – Správa ticketov (Mobilná brána)", version="0.1.0")
    sluzba = SluzbaTicketov(uloziste, odosielatel)

    # --- korelačný identifikátor ---------------------------------------------------------------
    @app.middleware("http")
    async def _korelacia(request: Request, call_next):
        odpoved = await call_next(request)
        cid = request.headers.get("X-Correlation-ID")
        if cid:
            odpoved.headers["X-Correlation-ID"] = cid
        return odpoved

    # --- chyby → problem+json --------------------------------------------------------------------
    @app.exception_handler(ProblemTicketu)
    async def _problem_ticketu(_: Request, e: ProblemTicketu):
        return _problem(e.status, e.titulok, e.pravidlo, e.detail, e.chybajuce_udaje)

    @app.exception_handler(_Neprihlaseny)
    async def _neprihlaseny(_: Request, __: _Neprihlaseny):
        return _problem(401, "Chýba alebo je neplatné prihlásenie")

    @app.exception_handler(RequestValidationError)
    async def _validacia(_: Request, e: RequestValidationError):
        chybajuce = sorted({".".join(str(x) for x in err["loc"][1:]) or str(err["loc"][0]) for err in e.errors()})
        pravidlo = "BR-006" if any("odovodnenie" in c for c in chybajuce) else "BR-005"
        return _problem(422, "Chýbajúce alebo neplatné údaje", pravidlo=pravidlo, chybajuce=chybajuce)

    # --- autentifikácia (QR-001) ---------------------------------------------------------------
    def pouzivatel(authorization: Annotated[Optional[str], Header()] = None) -> Pouzivatel:
        if not authorization or not authorization.lower().startswith("bearer "):
            raise _Neprihlaseny()
        p = overovac.over(authorization[7:].strip())
        if p is None:
            raise _Neprihlaseny()
        return p

    Prihlaseny = Annotated[Pouzivatel, Depends(pouzivatel)]

    # --- operácie ------------------------------------------------------------------------------
    @app.post("/api/v1/tickets", operation_id="podatTicket", status_code=201)
    def podat_ticket(
        telo: NovyTicket, p: Prihlaseny,
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=128)],
    ):
        t, _ = sluzba.podaj(p, idempotency_key, telo.predmet, telo.popis, telo.adresat.typ, telo.adresat.vyucujuciId)
        return JSONResponse(_ticket_json(t), status_code=201, headers={"Location": f"/api/v1/tickets/{t.id}"})

    @app.get("/api/v1/tickets", operation_id="zoznamTicketov")
    def zoznam_ticketov(p: Prihlaseny, stav: Annotated[Optional[StavTicketu], Query()] = None):
        return {"polozky": [_ticket_json(t) for t in sluzba.zoznam(p, stav)]}

    @app.get("/api/v1/tickets/{ticketId}", operation_id="detailTicketu")
    def detail_ticketu(ticketId: str, p: Prihlaseny):
        return _ticket_json(sluzba.detail(p, ticketId))

    @app.post("/api/v1/tickets/{ticketId}/prevzatie", operation_id="prevziatTicket")
    def prevziat_ticket(ticketId: str, p: Prihlaseny):
        return _ticket_json(sluzba.prevezmi(p, ticketId))

    @app.post("/api/v1/tickets/{ticketId}/rozhodnutie", operation_id="rozhodnutTicket")
    def rozhodnut_ticket(ticketId: str, telo: Rozhodnutie, p: Prihlaseny):
        return _ticket_json(sluzba.rozhodni(p, ticketId, telo.vysledok, telo.odovodnenie))

    return app

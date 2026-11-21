# SDD: generované z specification 0.2.1 · contract API-Tickets 0.1.0 (approved) · baseline B-01 · prompt implement-change v1.0 · 2026-11-21
"""Testovacie prostredie: testovacie tokeny (Q-10b), testovacia náhrada notifikačnej služby (ADR-003)
a kontrola KAŽDEJ odpovede voči approved contractu API-Tickets 0.1.0."""

import pathlib
import re
import uuid

import pytest
import yaml
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from mobilna_brana.api import create_app
from mobilna_brana.identity import Pouzivatel, ROLA_STUDENT, ROLA_STUDIJNE_ODDELENIE, ROLA_VYUCUJUCI
from mobilna_brana.tickety.uloziste import Uloziste

KOREN = pathlib.Path(__file__).resolve().parents[1]
CONTRACT_CESTA = KOREN / "spec/contracts/approved/api-tickets.openapi.yaml"
CONTRACT = yaml.safe_load(CONTRACT_CESTA.read_text(encoding="utf-8"))
_REGISTRY = Registry().with_resource("urn:api-tickets", Resource.from_contents(CONTRACT, default_specification=DRAFT202012))

POUZIVATELIA = {
    "t-student-1": Pouzivatel("stu-1", ROLA_STUDENT),
    "t-student-2": Pouzivatel("stu-2", ROLA_STUDENT),
    "t-vyucujuci-1": Pouzivatel("vyu-1", ROLA_VYUCUJUCI),
    "t-vyucujuci-2": Pouzivatel("vyu-2", ROLA_VYUCUJUCI),
    "t-so-1": Pouzivatel("so-1", ROLA_STUDIJNE_ODDELENIE),
    "t-so-2": Pouzivatel("so-2", ROLA_STUDIJNE_ODDELENIE),
}


class TestovaciOverovac:
    __test__ = False

    def over(self, token):
        return POUZIVATELIA.get(token)


class TestovaciOdosielatel:
    __test__ = False

    """Náhrada TS-NotifikacnaSluzba (NODE-FCM)."""

    def __init__(self):
        self.odoslane = []
        self.nedostupna = False

    def odosli(self, prijemca_id, ticket_id, stav):
        if self.nedostupna:
            raise ConnectionError("notifikačná služba nedostupná")
        self.odoslane.append((prijemca_id, ticket_id, stav))


def _operacia(metoda, cesta):
    """Nájde operáciu v approved contracte podľa metódy a cesty."""
    relativna = cesta.split("?")[0].removeprefix("/api/v1")
    for vzor, polozka in CONTRACT["paths"].items():
        regex = "^" + re.sub(r"\{[^}]+\}", "[^/]+", vzor) + "$"
        if re.match(regex, relativna) and metoda.lower() in polozka:
            return polozka[metoda.lower()]
    raise AssertionError(f"{metoda} {cesta} nie je v approved contracte")


def _schema_odpovede(operacia, status):
    odpovede = operacia["responses"]
    assert str(status) in odpovede, f"{operacia['operationId']}: status {status} nie je v contracte ({list(odpovede)})"
    odpoved = odpovede[str(status)]
    if "$ref" in odpoved:
        odpoved = CONTRACT["components"]["responses"][odpoved["$ref"].split("/")[-1]]
    (media, obsah), = odpoved["content"].items()
    return media, obsah["schema"]


def _ref_na_urn(schema):
    if isinstance(schema, dict):
        return {k: ("urn:api-tickets" + v if k == "$ref" else _ref_na_urn(v)) for k, v in schema.items()}
    if isinstance(schema, list):
        return [_ref_na_urn(x) for x in schema]
    return schema


class KlientSKontrolouContractu:
    """Obal TestClient: každá odpoveď musí mať status a telo podľa approved contractu."""

    def __init__(self, klient):
        self._k = klient
        self.kontrolovane_operacie = set()

    def volaj(self, metoda, cesta, token=None, json=None, hlavicky=None):
        h = dict(hlavicky or {})
        if token:
            h["Authorization"] = f"Bearer {token}"
        r = self._k.request(metoda, cesta, json=json, headers=h)
        op = _operacia(metoda, cesta)
        media, schema = _schema_odpovede(op, r.status_code)
        assert r.headers["content-type"].startswith(media), (op["operationId"], r.headers["content-type"])
        Draft202012Validator(_ref_na_urn(schema), registry=_REGISTRY).validate(r.json())
        self.kontrolovane_operacie.add((op["operationId"], r.status_code))
        return r

    # skratky podľa operationId
    def podat(self, token, telo=None, kluc=None, **kw):
        telo = telo if telo is not None else {
            "predmet": "Potvrdenie o štúdiu", "popis": "Potrebujem potvrdenie pre štipendium.",
            "adresat": {"typ": "studijne_oddelenie"}}
        hl = {"Idempotency-Key": kluc or f"kluc-{uuid.uuid4()}"}
        return self.volaj("POST", "/api/v1/tickets", token, json=telo, hlavicky=hl, **kw)

    def zoznam(self, token, stav=None):
        return self.volaj("GET", "/api/v1/tickets" + (f"?stav={stav}" if stav else ""), token)

    def detail(self, token, tid):
        return self.volaj("GET", f"/api/v1/tickets/{tid}", token)

    def prevziat(self, token, tid):
        return self.volaj("POST", f"/api/v1/tickets/{tid}/prevzatie", token)

    def rozhodnut(self, token, tid, vysledok, odovodnenie=None):
        telo = {"vysledok": vysledok}
        if odovodnenie is not None:
            telo["odovodnenie"] = odovodnenie
        return self.volaj("POST", f"/api/v1/tickets/{tid}/rozhodnutie", token, json=telo)


@pytest.fixture
def uloziste():
    return Uloziste()


@pytest.fixture
def notifikacie():
    return TestovaciOdosielatel()


@pytest.fixture
def api(uloziste, notifikacie):
    app = create_app(uloziste, TestovaciOverovac(), notifikacie)
    return KlientSKontrolouContractu(TestClient(app))

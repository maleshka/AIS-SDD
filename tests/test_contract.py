# SDD: generované z specification 0.2.1 · contract API-Tickets 0.1.0 (approved) · baseline B-01 · prompt implement-change v1.0 · 2026-11-21
"""Contract testy: implementácia zodpovedá approved contractu API-Tickets 0.1.0."""

from openapi_spec_validator import validate

from conftest import CONTRACT
from mobilna_brana.api import create_app
from mobilna_brana.tickety.uloziste import Uloziste
from conftest import TestovaciOdosielatel, TestovaciOverovac


def _operacie_contractu():
    return {(m.upper(), "/api/v1" + p, o["operationId"])
            for p, polozka in CONTRACT["paths"].items() for m, o in polozka.items()}


def _operacie_implementacie():
    app = create_app(Uloziste(), TestovaciOverovac(), TestovaciOdosielatel())
    spec = app.openapi()
    return {(m.upper(), p, o["operationId"]) for p, polozka in spec["paths"].items() for m, o in polozka.items()}


def test_approved_contract_je_platne_openapi():
    validate(CONTRACT)
    assert CONTRACT["info"]["version"] == "0.1.0"
    assert CONTRACT["info"]["x-status"] == "approved"


def test_implementacia_ma_presne_operacie_contractu():
    assert _operacie_implementacie() == _operacie_contractu()


def test_kazda_operacia_ma_mapping_na_sdd():
    for polozka in CONTRACT["paths"].values():
        for o in polozka.values():
            assert o["x-sdd"]["roles"] and o["x-sdd"]["rules"] and o["x-sdd"]["scenarios"], o["operationId"]

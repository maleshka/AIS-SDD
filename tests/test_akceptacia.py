# SDD: generované z specification 0.2.1 · contract API-Tickets 0.1.0 (approved) · baseline B-01 · prompt implement-change v1.0 · 2026-11-21
"""Acceptance testy pre spec/stories/features/US-002.feature (SC-002-01 … SC-002-11)
a invarianty BR-001, BR-003. Každá odpoveď sa zároveň kontroluje voči approved contractu (conftest)."""

import threading

STUDENT, STUDENT2 = "t-student-1", "t-student-2"
VYU, VYU2 = "t-vyucujuci-1", "t-vyucujuci-2"
SO, SO2 = "t-so-1", "t-so-2"


def _ticket_pre_vyucujuceho(api, vyucujuci_id="vyu-1"):
    r = api.podat(STUDENT, {"predmet": "Uznanie predmetu", "popis": "Prosím o uznanie.",
                            "adresat": {"typ": "vyucujuci", "vyucujuciId": vyucujuci_id}})
    return r.json()["id"]


def _ticket_v_posudzovani(api, posudzovatel=SO):
    tid = api.podat(STUDENT).json()["id"]
    assert api.prevziat(posudzovatel, tid).status_code == 200
    return tid


# --- SC-002-01 -----------------------------------------------------------------------------------
def test_SC_002_01_student_poda_uplny_ticket(api):
    r = api.podat(STUDENT)
    assert r.status_code == 201
    t = r.json()
    assert t["stav"] == "podany"
    assert r.headers["Location"] == f"/api/v1/tickets/{t['id']}"
    assert [x["id"] for x in api.zoznam(STUDENT).json()["polozky"]] == [t["id"]]


# --- SC-002-02 -----------------------------------------------------------------------------------
def test_SC_002_02_neuplny_ticket_sa_neprijme(api):
    r = api.podat(STUDENT, {"predmet": "Bez popisu", "adresat": {"typ": "studijne_oddelenie"}})
    assert r.status_code == 422
    assert "popis" in r.json()["chybajuceUdaje"]
    assert r.json()["pravidlo"] == "BR-005"
    assert api.zoznam(STUDENT).json()["polozky"] == []


def test_SC_002_02_adresat_vyucujuci_bez_id_sa_neprijme(api):
    r = api.podat(STUDENT, {"predmet": "X", "popis": "Y", "adresat": {"typ": "vyucujuci"}})
    assert r.status_code == 422


# --- SC-002-03 -----------------------------------------------------------------------------------
def test_SC_002_03_student_sleduje_stav(api):
    tid = _ticket_v_posudzovani(api)
    r = api.detail(STUDENT, tid)
    assert r.status_code == 200
    assert r.json()["stav"] == "v_posudzovani"
    assert r.json()["posudzovatelId"] == "so-1"


# --- SC-002-04, invariant BR-003 -------------------------------------------------------------------
def test_SC_002_04_student_nevidi_cudzi_ticket(api):
    tid = api.podat(STUDENT).json()["id"]
    r = api.detail(STUDENT2, tid)
    assert r.status_code == 404
    assert r.json()["pravidlo"] == "BR-003"
    assert api.zoznam(STUDENT2).json()["polozky"] == []


def test_BR_003_ticket_vidi_iba_zvoleny_vyucujuci(api):
    tid = _ticket_pre_vyucujuceho(api, "vyu-1")
    assert api.detail(VYU, tid).status_code == 200
    assert api.detail(VYU2, tid).status_code == 404
    assert api.detail(SO, tid).status_code == 404
    assert api.zoznam(VYU2).json()["polozky"] == []


def test_BR_003_ticket_pre_so_vidi_kazdy_zamestnanec_so(api):
    tid = api.podat(STUDENT).json()["id"]
    assert api.detail(SO, tid).status_code == 200
    assert api.detail(SO2, tid).status_code == 200
    assert api.detail(VYU, tid).status_code == 404


# --- SC-002-05 -----------------------------------------------------------------------------------
def test_SC_002_05_posudzovatel_schvali_a_ziadatel_dostane_oznamenie(api, notifikacie):
    tid = _ticket_v_posudzovani(api)
    assert notifikacie.odoslane == []            # pri prevzatí sa neposiela (Q-07)
    r = api.rozhodnut(SO, tid, "schvaleny")
    assert r.status_code == 200
    assert r.json()["stav"] == "schvaleny"
    assert notifikacie.odoslane == [("stu-1", tid, "schvaleny")]


# --- SC-002-06 -----------------------------------------------------------------------------------
def test_SC_002_06_zamietnutie_s_odovodnenim(api, notifikacie):
    tid = _ticket_pre_vyucujuceho(api)
    api.prevziat(VYU, tid)
    r = api.rozhodnut(VYU, tid, "zamietnuty", "Predmet nemožno uznať.")
    assert r.status_code == 200
    d = api.detail(STUDENT, tid).json()
    assert d["stav"] == "zamietnuty"
    assert d["odovodnenie"] == "Predmet nemožno uznať."
    assert notifikacie.odoslane == [("stu-1", tid, "zamietnuty")]


# --- SC-002-07, invariant BR-001 -------------------------------------------------------------------
def test_SC_002_07_rozhodnuty_ticket_sa_neda_znovu_rozhodnut(api):
    tid = _ticket_v_posudzovani(api)
    api.rozhodnut(SO, tid, "schvaleny")
    r = api.rozhodnut(SO, tid, "zamietnuty", "Zmena názoru.")
    assert r.status_code == 409
    assert r.json()["pravidlo"] == "BR-001"
    assert api.detail(STUDENT, tid).json()["stav"] == "schvaleny"
    assert api.prevziat(SO, tid).status_code == 409


def test_BR_001_pri_subehu_plati_iba_prve_rozhodnutie(api, uloziste):
    tid = _ticket_v_posudzovani(api)
    vysledky = []

    def rozhodni(v):
        vysledky.append(api.rozhodnut(SO, tid, v, "dôvod").status_code)

    vlakna = [threading.Thread(target=rozhodni, args=(v,)) for v in ["schvaleny", "zamietnuty"] * 4]
    for v in vlakna:
        v.start()
    for v in vlakna:
        v.join()
    assert sorted(vysledky) == [200] + [409] * 7
    prechody = [a for a in uloziste.audit(tid) if a["z_stavu"] == "v_posudzovani"]
    assert len(prechody) == 1


# --- SC-002-08 -----------------------------------------------------------------------------------
def test_SC_002_08_ziadatel_nemoze_rozhodnut(api):
    tid = _ticket_v_posudzovani(api)
    r = api.rozhodnut(STUDENT, tid, "schvaleny")
    assert r.status_code == 403
    assert r.json()["pravidlo"] == "BR-002"
    assert api.detail(STUDENT, tid).json()["stav"] == "v_posudzovani"


def test_BR_002_ziadatel_nemoze_prevziat_a_posudzovatel_nemoze_podat(api):
    tid = api.podat(STUDENT).json()["id"]
    assert api.prevziat(STUDENT, tid).status_code == 403
    assert api.podat(SO).status_code == 403


# --- SC-002-09 -----------------------------------------------------------------------------------
def test_SC_002_09_zamietnutie_bez_odovodnenia_sa_neprijme(api, notifikacie):
    tid = _ticket_v_posudzovani(api)
    r = api.rozhodnut(SO, tid, "zamietnuty")
    assert r.status_code == 422
    assert r.json()["pravidlo"] == "BR-006"
    assert api.detail(STUDENT, tid).json()["stav"] == "v_posudzovani"
    assert notifikacie.odoslane == []


# --- SC-002-10 -----------------------------------------------------------------------------------
def test_SC_002_10_opakovane_odoslanie_nevytvori_druhy_ticket(api):
    prvy = api.podat(STUDENT, kluc="kluc-opakovanie-1")
    druhy = api.podat(STUDENT, kluc="kluc-opakovanie-1")
    assert prvy.status_code == druhy.status_code == 201
    assert prvy.json()["id"] == druhy.json()["id"]
    assert len(api.zoznam(STUDENT).json()["polozky"]) == 1


def test_Q_11_rovnaky_kluc_s_inym_obsahom_je_konflikt(api):
    api.podat(STUDENT, kluc="kluc-opakovanie-2")
    r = api.podat(STUDENT, {"predmet": "Iné", "popis": "Iný obsah", "adresat": {"typ": "studijne_oddelenie"}},
                  kluc="kluc-opakovanie-2")
    assert r.status_code == 409
    assert len(api.zoznam(STUDENT).json()["polozky"]) == 1


# --- SC-002-11 -----------------------------------------------------------------------------------
def test_SC_002_11_vypadok_notifikacii_nezrusi_rozhodnutie(api, notifikacie, uloziste):
    tid = _ticket_v_posudzovani(api)
    notifikacie.nedostupna = True
    r = api.rozhodnut(SO, tid, "schvaleny")
    assert r.status_code == 200
    assert api.detail(STUDENT, tid).json()["stav"] == "schvaleny"
    assert [z["ticket_id"] for z in uloziste.zlyhania_notifikacii()] == [tid]   # QR-003


# --- Q-19 (BR-004) ---------------------------------------------------------------------------------
def test_Q_19_rozhoduje_iba_ten_kto_prevzal(api):
    tid = _ticket_v_posudzovani(api, posudzovatel=SO)
    assert api.prevziat(SO2, tid).status_code == 409
    r = api.rozhodnut(SO2, tid, "schvaleny")
    assert r.status_code == 403
    assert r.json()["pravidlo"] == "BR-004"
    assert api.rozhodnut(SO, tid, "schvaleny").status_code == 200


def test_BR_004_nemozno_rozhodnut_neprevzaty_ticket(api):
    tid = api.podat(STUDENT).json()["id"]
    r = api.rozhodnut(SO, tid, "schvaleny")
    assert r.status_code == 409
    assert r.json()["pravidlo"] == "BR-004"


# --- QR-001, QR-002, QR-004 ------------------------------------------------------------------------
def test_QR_001_bez_prihlasenia_401(api):
    assert api.zoznam(None).status_code == 401
    assert api.zoznam("neplatny-token").status_code == 401


def test_QR_002_kazda_zmena_stavu_ma_audit(api, uloziste):
    tid = _ticket_v_posudzovani(api)
    api.rozhodnut(SO, tid, "zamietnuty", "Nie.")
    prechody = [(a["z_stavu"], a["do_stavu"], a["kto"]) for a in uloziste.audit(tid)]
    assert prechody == [(None, "podany", "stu-1"), ("podany", "v_posudzovani", "so-1"),
                        ("v_posudzovani", "zamietnuty", "so-1")]


def test_QR_004_notifikacia_ani_log_neobsahuju_osobne_udaje(api, notifikacie, caplog):
    tid = _ticket_v_posudzovani(api)
    notifikacie.nedostupna = True
    api.rozhodnut(SO, tid, "zamietnuty", "Tajné odôvodnenie")
    log = caplog.text
    assert tid in log
    assert "Potvrdenie o štúdiu" not in log and "Tajné odôvodnenie" not in log and "stu-1" not in log


def test_filter_podla_stavu(api):
    t1 = api.podat(STUDENT).json()["id"]
    api.podat(STUDENT)
    api.prevziat(SO, t1)
    polozky = api.zoznam(STUDENT, "v_posudzovani").json()["polozky"]
    assert [p["id"] for p in polozky] == [t1]

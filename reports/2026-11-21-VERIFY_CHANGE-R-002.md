# VERIFY_CHANGE – validation report R-002

Dátum: 2026-11-21 · Prompt: spec/prompts/verify-change.md v1.0 · Pripravila: AI (Claude)
Specification **0.2.1** (approved) · Approved contract **API-Tickets 0.1.0** · Architecture baseline B-01

V tomto režime sa nemenila specification, contract, code, tests ani rozhodnutia. Report iba zaznamenáva výsledky kontrol.

## Výsledky kontrol

| # | Kontrola | Výsledok | Dôkaz |
|---|---|---|---|
| 1 | Syntax YAML všetkých súborov spec/ | **PASS** | reports/2026-11-21-spec-check.txt (17+ súborov, PASS) |
| 2 | Approved contract je platné OpenAPI 3.1 | **PASS** | tests/test_contract.py::test_approved_contract_je_platne_openapi |
| 3 | Existencia všetkých použitých IDs | **PASS** | tools/check_spec.py – všetky IDs definované |
| 4 | Traceability G-002 → R-002 → … → test | **PASS** | spec/traceability/traceability.yaml (motivácia → business → application → contract → code → test) |
| 5 | Service Realization a Application Usage | **PASS** | BP-VybavovanieTicketu ← AS-SpravaTicketov ← AC-MobilnaBrana; service-realization.yaml (approved), views B-01 |
| 6 | Component boundaries (ADR-001) | **PASS** | kód iba v src/mobilna_brana (AC-MobilnaBrana); klient AC-ManazmentTicketov negenerovaný |
| 7 | Allowed dependencies | **PASS** | importy: štandardná knižnica, fastapi, pydantic; žiadny prístup k AC-UIS; notifikácie iba cez rozhranie OdosielatelNotifikacii (INT-003) |
| 8 | Zhoda kódu s approved contractom – operácie | **PASS** | test_implementacia_ma_presne_operacie_contractu (5 = 5, cesty, metódy, operationId) |
| 9 | Zhoda kódu s approved contractom – odpovede | **PASS** | každá odpoveď v 23 acceptance testoch overená voči status kódom a JSON schéme contractu (tests/conftest.py); kontrola preukázateľne zachytí chybné telo aj nedeklarovaný status |
| 10 | Pokrytie scenárov SC-002-01…SC-002-11 | **PASS** | 11/11 – reports/2026-11-21-test-results.txt |
| 11 | Invariant BR-001 (aj pri súbehu) | **PASS** | test_SC_002_07…, test_BR_001_pri_subehu_plati_iba_prve_rozhodnutie (8 súbežných rozhodnutí → 1× 200, 7× 409, 1 auditný prechod) |
| 12 | Invariant BR-003 | **PASS** | test_SC_002_04…, test_BR_003_ticket_vidi_iba_zvoleny_vyucujuci, test_BR_003_ticket_pre_so_vidi_kazdy_zamestnanec_so |
| 13 | Quality: QR-001 security, QR-002 audit, QR-003 notifikácie, QR-004 privacy | **PASS** | test_QR_001…, test_QR_002…, test_SC_002_11…, test_QR_004… |
| 14 | QR-005 výkon a dostupnosť | **UNKNOWN** | čísla nie sú v specification určené (Q-15) – nemerané |
| 15 | Stav ADR | **PASS** | ADR-001…ADR-004: Accepted |
| 16 | Otvorené DECISION REQUIRED pre R-002 | **PASS** | žiadne; zostávajú neblokujúce Q-09, Q-15–Q-18 |
| 17 | Deployment: väzba ART-BackendMobilnejBrany → AC-MobilnaBrana v modeli | **FAIL** | v modeli B-01 väzba chýba (Q-09, MF-02); deployment.yaml ju uvádza ako NEOVERENÚ |
| 18 | Deployable Artifact | **not applicable** | deployment.yaml (approved): `deployable_artifact_required: false` |
| 19 | Vlastníci pravidiel a quality requirements | **FAIL** | `owner: null` pri C-001, BR-003, QR-001…QR-005 (Q-18) |
| 20 | Produkčné napojenie identity (Q-10b) a FCM | **UNKNOWN** | mimo rozsahu výrezu; v testoch testovacie náhrady (ADR-003, ADR-004) |
| 21 | Enterprise Continuum, Implementation & Migration | **UNKNOWN** | reuse-catalog.yaml a implementation-context.yaml ostávajú draft (vlastník/verzia UNKNOWN, Q-17) |
| 22 | Jeden konzistentný pull request | **FAIL** | projekt zatiaľ nie je v git repozitári; approval.yaml `approved_in_pull_request: null` |

**Súhrn:** 16× PASS · 3× FAIL · 3× UNKNOWN · 1× not applicable.
Funkčná zmena R-002 je overená (kontroly 1–13). FAIL položky sa týkajú modelu v EA (17), chýbajúcich vlastníkov (19)
a chýbajúceho PR (22), nie správania kódu.

## Testy

`26 passed` (pytest, Python 3.14) – zoznam v reports/2026-11-21-test-results.txt.
Spustenie: `.venv/bin/python -m pytest -v`

## Čo treba urobiť pre uzavretie (Gate 7)

1. Q-09: v Sparx EA doplniť `Backend mobilnej brány —Realization→ Mobilná brána` (kontrola 17).
2. Q-18: doplniť vlastníkov pri C-001, BR-003, QR-001…QR-005 (kontrola 19).
3. Založiť git repozitár, spojiť specification, contract, code, tests a reporty do jedného PR (kontrola 22)
   a po review označiť nový baseline.
4. Človek potvrdí business význam zmeny (AGENTS.md kap. 16 – IMPLEMENT_CHANGE DoD).

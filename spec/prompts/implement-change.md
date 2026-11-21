# PROMPT TEMPLATE – IMPLEMENT_CHANGE · v1.1

Predpoklad: spec/contracts/approved/approval.yaml obsahuje schválenú verziu contractu (vyplnil človek).

```
Mode: IMPLEMENT_CHANGE
Role: Implementer – generuje candidate code a tests v hraniciach architektúry.
Change ID: <R-xxx alebo CR-xxx>
Specification baseline: <schválená verzia>
Approved contract: API-Tickets <schválená verzia>

Authoritative inputs (presné súbory a verzie):
  - spec/contracts/approved/api-tickets.openapi.yaml + approval.yaml
  - spec/requirements/business-rules.yaml, spec/application/lifecycles.yaml, spec/stories/features/*.feature
  - spec/application/components.yaml (hranice, allowed_dependencies), ADR-001…ADR-00x (Accepted)

Allowed scope:
  - mení iba src/mobilna_brana/**, tests/**, requirements.txt, pytest.ini, reports/,
    spec/traceability/traceability.yaml (iba sekcia code → test)
  - NEMENÍ contract, authoritative spec, ADR; nepridáva závislosť na AC-UIS ani nový System Software bez ADR
  - každý generovaný súbor má hlavičku: specification, contract, baseline, verzia promptu

Required outputs:
  - reports/<dátum>-IMPLEMENT_CHANGE-plan-<Change ID>.md (generation plan po súboroch) – pred kódom
  - candidate code + acceptance testy pre každý scenár + contract testy
  - aktualizovaná traceability (scenár / BR / QR → test)

Checks (príkazy a očakávaný dôkaz):
  - .venv/bin/python -m pytest -v → všetky testy PASS, uložiť do reports/<dátum>-test-results.txt
  - test_implementacia_ma_presne_operacie_contractu → PASS
  - každá odpoveď v testoch overená voči schéme contractu (tests/conftest.py)
  - .venv/bin/python tools/check_spec.py . → RESULT: PASS

Decision rule:
  STOP and ask (DECISION REQUIRED), ak implementácia odhalí chýbajúce rozhodnutie alebo chybu contractu –
  vtedy späť do DESIGN_CONTRACT, contract nemeň.
```

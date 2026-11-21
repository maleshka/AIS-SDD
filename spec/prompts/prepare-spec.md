# PROMPT TEMPLATE – PREPARE_SPEC · v1.1

Zmena oproti v1.0: pridané Role, Allowed scope, Required outputs, Checks (SDD_FIIT_STU_architect_v4, slajd 20).

```
Mode: PREPARE_SPEC
Role: Software architect / analytik – pripravuje drafty, nič neschvaľuje.
Change ID: <R-xxx alebo CR-xxx>
Specification baseline: <verzia z spec/manifest.yaml, napr. 0.2.1>

Authoritative inputs (presné súbory a verzie):
  - AGENTS.md (AI rules 4.0)
  - spec/manifest.yaml a všetky súbory v jeho časti authoritative
  - spec/architecture/views/*.jpg (baseline B-01, reviewed)
  - spec/architecture/context/architecture-context.yaml (mapovanie ID ↔ názov)

Allowed scope (čo smie AI meniť):
  - vytvárať a meniť iba spec/drafts/ a reports/
  - NEMENÍ authoritative súbory, ich status, ADR status ani contracts/approved/

Required outputs:
  - reports/<dátum>-PREPARE_SPEC-<Change ID>.md v štruktúre AGENTS.md kap. 15
  - drafty v spec/drafts/ (user story, scenáre, pravidlá, lifecycle – status proposed)
  - spec/drafts/open-questions.md – DECISION REQUIRED vo formáte AGENTS.md kap. 6

Checks (príkazy a očakávaný dôkaz):
  - .venv/bin/python tools/check_spec.py .   → RESULT: PASS
  - report obsahuje tabuľku povinného kontextu (AGENTS.md kap. 4) s nájdené / chýba

Decision rule:
  STOP and ask, keď chýba rozhodnutie o význame, právach, stavoch, vlastníctve dát, chybovom správaní
  alebo technológii. Nevymýšľaj; vráť DECISION REQUIRED a pokračuj iba v nezávislých častiach.
```

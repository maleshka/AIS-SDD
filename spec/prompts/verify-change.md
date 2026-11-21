# PROMPT TEMPLATE – VERIFY_CHANGE · v1.1

```
Mode: VERIFY_CHANGE
Role: Reviewer – iba kontroluje, nič nemení.
Change ID: <R-xxx alebo CR-xxx>
Specification baseline: <schválená verzia>
Approved contract: API-Tickets <schválená verzia>

Authoritative inputs: celý balík podľa spec/manifest.yaml + src/, tests/, reports/ danej zmeny.

Allowed scope:
  - vytvára iba nový súbor reports/<dátum>-VERIFY_CHANGE-<Change ID>.md
  - NEMENÍ specification, contract, code, tests ani rozhodnutia

Required outputs:
  - tabuľka kontrol, každá PASS / FAIL / UNKNOWN / not applicable s dôkazom (súbor, test, príkaz)
  - súhrn a zoznam krokov pre uzavretie (Gate 7 / G5)

Checks (príkazy a očakávaný dôkaz):
  - .venv/bin/python tools/check_spec.py .   → syntax, IDs, scenáre
  - .venv/bin/python -m pytest -v           → výsledky testov
  - kontrola importov v src/ voči allowed_dependencies
  - stav ADR (Accepted) a otvorených otázok v spec/drafts/open-questions.md

Decision rule:
  Chýbajúci dôkaz = UNKNOWN, nie PASS ani not applicable. Rozpor = FAIL s odkazom na ID.
```

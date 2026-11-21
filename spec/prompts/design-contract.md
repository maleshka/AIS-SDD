# PROMPT TEMPLATE – DESIGN_CONTRACT · v1.1

Predpoklad: Gates 1–5 splnené (authoritative súbory approved, ADR Accepted, contract-design-profile approved).

```
Mode: DESIGN_CONTRACT
Role: Software architect – navrhuje contract, neschvaľuje ho.
Change ID: <R-xxx alebo CR-xxx>
Specification baseline: <schválená verzia, napr. 0.2.1>

Authoritative inputs (presné súbory a verzie):
  - AGENTS.md (AI rules 4.0), spec/manifest.yaml
  - spec/policies/contract-design-profile.yaml (approved)
  - spec/requirements/*, spec/business/*, spec/application/*, spec/technology/* (approved)
  - spec/stories/features/*.feature, spec/architecture/decisions/ADR-*.md (Accepted)
  - pri zmene existujúceho contractu: spec/contracts/approved/<súbor> (aktuálna approved verzia)

Allowed scope:
  - zapisuje iba do spec/contracts/proposed/ a reports/
  - NEMENÍ spec/contracts/approved/, approval.yaml ani authoritative súbory

Required outputs:
  - spec/contracts/proposed/<api>.openapi.yaml (OpenAPI 3.1, info.x-status: proposed)
  - spec/contracts/proposed/contract-mapping.yaml (každá operácia → R, AS, AC, BP, BR, SC, DO)
  - reports/<dátum>-DESIGN_CONTRACT-<Change ID>.md s impact analysis a approval checklistom (AGENTS.md kap. 9)
  - pri zmene verzie: zoznam breaking / non-breaking zmien podľa spec/policies/versioning.md

Checks (príkazy a očakávaný dôkaz):
  - openapi-spec-validator nad proposed súborom → bez chýb
  - každý scenár a každé BR má aspoň jednu operáciu → PASS
  - status kódy a formát chýb podľa contract-design-profile.yaml → PASS
  - .venv/bin/python tools/check_spec.py . → RESULT: PASS

Decision rule:
  STOP and ask, keď specification neurčuje API vs. event, oprávnenie, error behavior, idempotency,
  lifecycle prechod alebo compatibility. Contract závislý od otvorenej otázky negeneruj.
```

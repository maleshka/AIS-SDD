# VERIFY_CHANGE – opakované overenie R-002

Dátum: 2026-11-23 · Prompt: spec/prompts/verify-change.md v1.1 · Pripravila: AI (Claude), rozhodnutia: Anna-Mariia Malesh
Specification **0.3.0** (approved) · Approved contract **API-Tickets 0.1.0** · Architecture baseline B-01
Predchádzajúce overenie: reports/2026-11-21-VERIFY_CHANGE-R-002.md (16× PASS · 3× FAIL · 3× UNKNOWN · 1× not applicable)

V tomto režime sa nemenila specification, contract, code ani tests. Report zaznamenáva výsledky kontrol
a rozhodnutia človeka, ktoré uzavreli FAIL a UNKNOWN položky.

## Výsledky kontrol

Kontroly 1–13, 15 a 18 sa nezmenili oproti 2026-11-21. Testy aj kontrola balíka boli 2026-11-23 spustené znova.

| # | Kontrola | 21. 11. | 23. 11. | Dôkaz / rozhodnutie |
|---|---|---|---|---|
| 1–13 | Syntax, contract, IDs, traceability, boundaries, zhoda kódu s contractom, scenáre, BR-001, BR-003, QR-001…004 | PASS | **PASS** | `26 passed`; `tools/check_spec.py .` → RESULT: PASS |
| 14 | QR-005 výkon a dostupnosť | UNKNOWN | **not applicable** | Q-15: mimo rozsahu výrezu (quality-requirements.yaml) |
| 15 | Stav ADR | PASS | **PASS** | ADR-001…004 Accepted |
| 16 | Otvorené DECISION REQUIRED | PASS | **PASS** | spec/drafts/open-questions.md – všetky Q-01…Q-20 uzavreté |
| 17 | Väzba ART-BackendMobilnejBrany → AC-MobilnaBrana v modeli | FAIL | **PASS** | Q-09: Realization doplnená v EA (Technology Usage Viewpoint TO BE), Anna-Mariia Malesh, 2026-11-22; deployment.yaml, MF-02. Aktualizovaný obrázok `spec/architecture/views/B-01-technology-usage-to-be.jpg` je súčasťou tohto PR |
| 18 | Deployable Artifact | n/a | **not applicable** | `deployable_artifact_required: false` |
| 19 | Vlastníci pravidiel a quality requirements | FAIL | **PASS** | Q-18: owner doplnený pri C-001, BR-001…007, QR-001…006 |
| 20 | Produkčné napojenie identity a FCM | UNKNOWN | **not applicable** | rozhodnutie Anna-Mariia Malesh, 2026-11-23: mimo rozsahu výrezu; v kóde testovacie náhrady podľa ADR-003 a ADR-004 |
| 21 | Enterprise Continuum, Implementation & Migration | UNKNOWN | **PASS** | reuse-catalog.yaml a implementation-context.yaml schválené (Anna-Mariia Malesh, 2026-11-23); hodnoty UNKNOWN ponechané zámerne, model ani tím ich neuvádza |
| 22 | Jeden konzistentný pull request | FAIL | **PASS po zlúčení** | repozitár github.com/maleshka/AIS-SDD; tento PR (vetva verify/R-002) s reportom, schváleniami a obrázkom; číslo PR v approval.yaml |

**Súhrn:** 19× PASS · 0× FAIL · 0× UNKNOWN · 3× not applicable (14, 18, 20).
FAIL položky: 3/3 doriešené. UNKNOWN položky: 3/3 uzavreté (14 a 20 ako mimo výrezu, 21 schválením).

## Gate 7

Po review a zlúčení tohto PR do `main` je R-002 overená a uzavretá. Nový baseline označí tag na `main`.

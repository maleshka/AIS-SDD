# SDD – Moje štúdium extension: R-002 Ticket

Specification-Driven Development balík pre jednu end-to-end funkcionalitu: **študent vytvorí ticket a sleduje jeho
schválenie alebo zamietnutie**. Nadväzuje na architektonický model v Sparx EA
(`Moje_studium_extended_2026_11_21_v21.qea`, baseline **B-01**).

Specification **0.2.1 – approved** (Anna-Mariia Malesh, 2026-11-21) · Contract **API-Tickets 0.1.0 – approved**.

## Stav etáp

| Etapa | Stav | Hlavné súbory |
|---|---|---|
| 1 Problém a motivácia | approved | requirements.yaml, glossary.md, business/scenarios/BSC-002 |
| 2 Business proces a služba | approved | business/actors-processes.yaml |
| 3 Aplikačné služby a komponenty | approved (Q-01, Q-13) | application/*.yaml, ADR-001, ADR-002 |
| 4 Správanie, pravidlá, scenáre | approved (Q-03…Q-08, Q-11, Q-19), 11 scenárov | business-rules.yaml, lifecycles.yaml, stories/ |
| 5 Technológia a deployment | approved | technology/*.yaml, ADR-004 |
| 6 Contract | **approved** API-Tickets 0.1.0 | contracts/approved/, approval.yaml |
| 7 Implementácia a overenie | candidate code + 26 testov PASS; VERIFY: 16 PASS, 3 FAIL, 3 UNKNOWN | src/, tests/, reports/ |


## Priebeh (reporty)

PREPARE_SPEC → DESIGN_CONTRACT → schválenie contractu → IMPLEMENT_CHANGE (plán) → VERIFY_CHANGE – všetko v [reports/](reports/).
Prompty v [spec/prompts/](spec/prompts/).

## Spustenie testov

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -v
```

Výsledok overenia: [reports/2026-11-21-VERIFY_CHANGE-R-002.md](reports/2026-11-21-VERIFY_CHANGE-R-002.md).

## Ukážka v prehliadači

```bash
.venv/bin/python demo.py
```

Otvor http://127.0.0.1:8000/docs. Pri operácii klikni *Try it out* a do poľa `authorization` napíš
`Bearer t-student-1` (študent), `Bearer t-so-1` (študijné oddelenie) alebo `Bearer t-vyucujuci-1`.
Prihlásenie a notifikácie sú ukážkové (rovnaké ako v testoch); notifikácie sa vypisujú do terminálu.

## Kontrola balíka

```bash
python3 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
.venv/bin/python tools/check_spec.py .
```

Kontroluje syntax YAML, či každé použité ID je definované a či scenáre zodpovedajú R-002.

## Mimo SDD

FPA, nacenenie a harmonogram sú v projektovej dokumentácii: `../FPA_Moje_studium_extension.xlsx`.

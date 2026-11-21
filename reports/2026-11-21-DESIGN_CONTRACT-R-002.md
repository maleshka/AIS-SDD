# DESIGN_CONTRACT report – R-002

Dátum: 2026-11-21 · Prompt: spec/prompts/design-contract.md v1.0 · Pripravila: AI (Claude) · Stav výstupu: **proposed**

## Pochopenie úlohy

Navrhnúť HTTP contract pre AS-SpravaTicketov na rozhraní AIF-APIBrany (poskytuje AC-MobilnaBrana) tak, aby každá operácia
mala business dôvod v R-002 a bola namapovaná na proces, pravidlá, dáta a scenáre. Contract neschvaľujem.

## Režim a specification baseline

DESIGN_CONTRACT · specification **0.2.1** (approved; 0.2.0 schválila Anna-Mariia Malesh 2026-11-21, 0.2.1 = spresnenie BR-004
rozhodnutím Q-19 z toho istého dňa) · architecture baseline B-01.

## Použité autoritatívne vstupy

- spec/manifest.yaml (0.2.1), approved súbory etáp 1–5, ADR-001…ADR-004 (Accepted).
- spec/policies/contract-design-profile.yaml (approved 2026-11-21) – použité pravidlá: OpenAPI 3.1, `/api/v1`, camelCase,
  RFC 3339, UUID, problem+json, `X-Correlation-ID`, `Idempotency-Key`, mapovanie status kódov, bearer token.
- Obrázky views B-01 (approved, reviewed_by Anna-Mariia Malesh): Application Cooperation / Structure / Usage TO BE,
  Service Realization, Information Structure, Technology TO BE.

## Chýbajúce informácie alebo rozpory

- Rozpor *kto rozhoduje prevzatý ticket* → DECISION REQUIRED Q-19 → rozhodnuté (iba ten, kto prevzal), zapísané do BR-004.
- Žiadne ďalšie blokujúce otázky. Neblokujúce: Q-09, Q-15–Q-18.

## Impact analysis

```yaml
change:
  mode: "DESIGN_CONTRACT"
  requirement: "R-002"
  specification_baseline: "0.2.1"
  reason: "Návrh API-Tickets pre AS-SpravaTicketov (GAP-004, D-005)."
affected:
  goals: ["G-002"]
  actors_roles: ["ROLE-Ziadatel", "ROLE-Posudzovatel"]
  business_processes: ["BP-VytvorenieTicketu", "BP-PosudenieTicketu", "BP-OznamenieVysledku"]
  business_services: ["BS-VybavovanieTicketov"]
  application_services: ["AS-SpravaTicketov (new operations)", "AS-Notifikacie (side effect)"]
  application_components: ["AC-MobilnaBrana (provider)", "AC-ManazmentTicketov (consumer)"]
  interfaces_contracts: ["AIF-APIBrany", "API-Tickets 0.1.0 (new, proposed)"]
  data_objects: ["DO-Ticket", "DO-Notifikacia"]
  technology_elements: ["TS-NotifikacnaSluzba (used)", "ART-DatabazaMobilnejBrany (unchanged by contract)"]
  work_packages_deliverables: ["WP-004", "D-005"]
  decisions: ["ADR-001", "ADR-002", "ADR-003", "ADR-004", "Q-19"]
  scenarios: ["SC-002-01 … SC-002-11"]
  tests: []
open_questions: []
```

## Navrhovaný výstup

- `spec/contracts/proposed/api-tickets.openapi.yaml` – API-Tickets **0.1.0**, 5 operácií:

| operationId | HTTP | Kto | Prechod | Scenáre |
|---|---|---|---|---|
| podatTicket | POST /tickets | Žiadateľ | → podany | SC-01, 02, 10 |
| zoznamTicketov | GET /tickets | Žiadateľ, Posudzovateľ | – | SC-01, 04 |
| detailTicketu | GET /tickets/{ticketId} | Žiadateľ, Posudzovateľ | – | SC-03, 04, 06, 11 |
| prevziatTicket | POST /tickets/{ticketId}/prevzatie | Posudzovateľ (adresát) | podany → v_posudzovani | SC-03 |
| rozhodnutTicket | POST /tickets/{ticketId}/rozhodnutie | Posudzovateľ, ktorý prevzal | v_posudzovani → schvaleny / zamietnuty | SC-05…09, 11 |

- `spec/contracts/proposed/contract-mapping.yaml` – mapping každej operácie na R-002, AS, AC, BP, BR, SC, DO.

### Technické voľby v návrhu, ktoré schvaľuje človek

Tieto body nevyplývajú priamo zo špecifikácie ani z profilu; AI ich navrhla a sú súčasťou schválenia contractu:

1. **Názvy v slovenčine podľa glosára** (cesty `/prevzatie`, `/rozhodnutie`; polia `predmet`, `popis`, `adresat`, `stav`…).
2. **Maximálne dĺžky**: predmet 200, popis 5 000, odôvodnenie 2 000 znakov.
3. **Idempotency-Key je povinný** pri podaní; opakovanie s rovnakým kľúčom a obsahom vráti pôvodný ticket (201),
   rovnaký kľúč s iným obsahom → 409.
4. **Cudzí ticket → 404** (neprezradí sa existencia); žiadateľ, ktorý ticket vidí, ale chce rozhodnúť → 403.
5. **Ticket podáva iba študent** (rola Žiadateľ); posudzovateľ pri podaní dostane 403.
6. **`vyucujuciId`** je identifikátor z existujúcej identity; klient ho získa existujúcou službou *Vyhľadávanie ľudí* (AS-IS) –
   výber vyučujúceho nie je súčasťou API-Tickets.
7. **Auditná história sa cez API nevracia** – audit (QR-002) je interný záznam.
8. **Notifikácia** obsahuje iba `ticketId` a `stav` (QR-004) a nie je súčasťou HTTP contractu (INT-003).

## Validation results

| Kontrola | Výsledok | Dôkaz |
|---|---|---|
| OpenAPI 3.1 syntax a schéma | PASS | openapi-spec-validator bez chýb |
| Operácie v OpenAPI = operácie v mappingu | PASS | 5 = 5 |
| Každý scenár SC-002-01…11 má operáciu | PASS | contract-mapping.yaml `coverage` |
| Každé pravidlo BR-001…007 má operáciu | PASS | contract-mapping.yaml `coverage` |
| Status kódy iba podľa profilu | PASS | 200, 201, 401, 403, 404, 409, 422 |
| operationId lowerCamelCase | PASS | všetkých 5 |
| Chyby ako application/problem+json | PASS | všetky 4xx odpovede |
| Všetky použité IDs existujú | PASS | tools/check_spec.py |

## Approval checklist (AGENTS.md kap. 9)

| Podmienka | Stav |
|---|---|
| Každá operácia má business dôvod a Requirement ID | ✅ R-002, BP v mappingu |
| Každý prvok mapuje na Application Service a poskytujúci Component | ✅ AS-SpravaTicketov, AC-MobilnaBrana |
| Názvy používajú glossary | ✅ (bod 1 vyššie na potvrdenie) |
| Pozitívne aj negatívne scenáre majú pozorovateľný výsledok | ✅ 11 scenárov, 6 negatívnych |
| Rules, invariants a prechody sú vynútiteľné alebo overiteľné | ✅ 409/422/403/404 s `pravidlo` v odpovedi |
| Authentication, authorization, audit a citlivé údaje sú explicitné | ✅ bearerAuth, x-sdd.roles, QR-002, QR-004 |
| Error behavior a retry/idempotency sú jasné | ✅ problem+json, Idempotency-Key, 409 pri súbehu |
| Project policy je dodržaná | ✅ contract-design-profile.yaml |
| Breaking changes majú compatibility rozhodnutie | n/a – prvá verzia contractu |
| Všetky DECISION REQUIRED pre contract sú uzavreté | ✅ Q-01…Q-13, Q-19 |

## Traceability summary

G-002 → R-002 → BS-VybavovanieTicketov → BP-VybavovanieTicketu → AS-SpravaTicketov → AC-MobilnaBrana (AIF-APIBrany)
→ API-Tickets.{podatTicket, zoznamTicketov, detailTicketu, prevziatTicket, rozhodnutTicket} → SC-002-01…11.
Contract → code → test doplní IMPLEMENT_CHANGE.

## Decision required / ADR

Žiadne otvorené DECISION REQUIRED. Nové ADR netreba.
**Ďalší krok – človek:** skontrolovať contract a body 1–8, potom schváliť verziu 0.1.0
(presun do `spec/contracts/approved/` + `approval.yaml`). Až potom IMPLEMENT_CHANGE.

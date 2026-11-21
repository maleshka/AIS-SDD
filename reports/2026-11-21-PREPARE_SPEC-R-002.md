# PREPARE_SPEC report – R-002

Dátum: 2026-11-21 · Prompt: spec/prompts/prepare-spec.md v1.0 · Pripravila: AI (Claude) · Stav: **návrh na ľudskú kontrolu**

## Pochopenie úlohy

Pripraviť specification package pre jednu end-to-end funkcionalitu: študent vytvorí ticket a sleduje jeho schválenie alebo
zamietnutie (R-002), z existujúceho modelu B-01. Výstupom sú drafty a otázky, nie contract ani code.

## Režim a specification baseline

PREPARE_SPEC · specification 0.1.0 (draft) · architecture baseline B-01 = `Moje_studium_extended_2026_11_21_v21.qea`.

## Použité autoritatívne vstupy

- Model B-01 – prvky, väzby a poznámky prečítané priamo zo súboru .qea (nie z obrázkov). Obrázky views zatiaľ nie sú
  exportované; pri review ich treba porovnať s týmto reportom.
- Odpovede autora projektu z 2026-11-21: Q-02, Q-04a, Q-10a, Q-14a (spec/drafts/open-questions.md).
- AGENTS.md (SDD AI rules 4.0), SDD_PROJECT_TEMPLATE v4.

## Kontrola povinného kontextu (AGENTS.md kap. 4)

| Položka | Stav | Kde |
|---|---|---|
| Goal a Requirement | nájdené (G-002, R-002) | requirements.yaml |
| Business Actor / Role | nájdené (ACT-Student, ROLE-Ziadatel, ROLE-Posudzovatel) | actors-processes.yaml |
| Business Process a Service | nájdené (BP-VybavovanieTicketu + 3 podprocesy, BS-VybavovanieTicketov) | actors-processes.yaml |
| Application Usage väzba | nájdené (AS-SpravaTicketov, AS-Notifikacie → BP-VybavovanieTicketu) | service-realization.yaml |
| Application Service a poskytujúci Component | **nejednoznačné** – dvaja realizátori | Q-01, ADR-001 |
| Service Realization | nájdené (BP → BS → R) | service-realization.yaml |
| Component responsibility, allowed dependencies | draft (závisí od Q-01) | components.yaml |
| Integračný kontext (Cooperation) | nájdené (AIF-APIBrany); komunikačný štýl na potvrdenie | interactions.yaml, Q-13 |
| Data Objects, ownership, lifecycle | DO-Ticket nájdený; vlastník závisí od Q-01; stavy rozhodnuté, prechod na potvrdenie | data-objects.yaml, lifecycles.yaml |
| Rules, invariants, scenarios | draft BR-001…BR-007, SC-002-01…08 (pozitívne aj negatívne) | business-rules.yaml, US-002.feature |
| Quality / security / privacy / audit | draft QR-001…QR-004; čísla neurčené (QR-005) | quality-requirements.yaml |
| ADR | ADR-001…004 – všetky Proposed | spec/architecture/decisions/ |
| Technology / Deployment | nájdené z modelu; chýba väzba Artifact → Component | technology-context.yaml, deployment.yaml, Q-09 |

## Chýbajúce informácie alebo rozpory

Blokujú contract (DECISION REQUIRED): **Q-01, Q-03, Q-04b, Q-05, Q-06, Q-07, Q-08**.
Blokujú implementáciu alebo kvalitu: Q-09, Q-10b, Q-11, Q-13.
Neblokujú R-002: Q-15, Q-16, Q-17.
Plné znenie s možnosťami a odporúčaním: spec/drafts/open-questions.md.

Zistenia z modelu: MF-01 (dvaja realizátori AS-SpravaTicketov), MF-02 (chýba deployment väzba), MF-03 (posudzovateľ nemá klienta).

## Impact analysis

```yaml
change:
  mode: "PREPARE_SPEC"
  requirement: "R-002"
  specification_baseline: "0.1.0"
  reason: "Nová funkcionalita – GAP-004 Chýbajúca správa ticketov."
affected:
  goals: ["G-002"]
  actors_roles: ["ROLE-Ziadatel", "ROLE-Posudzovatel"]
  business_processes: ["BP-VybavovanieTicketu", "BP-VytvorenieTicketu", "BP-PosudenieTicketu", "BP-OznamenieVysledku"]
  business_services: ["BS-VybavovanieTicketov"]
  application_services: ["AS-SpravaTicketov (new)", "AS-Notifikacie (modified)"]
  application_components: ["AC-MobilnaBrana (modified)", "AC-ManazmentTicketov (new)", "AC-MojeStudium (modified)"]
  interfaces_contracts: ["AIF-APIBrany (modified)", "API-Tickets (new, not yet designed)"]
  data_objects: ["DO-Ticket (new)", "DO-Notifikacia (modified)"]
  technology_elements: ["ART-DatabazaMobilnejBrany (new)", "SSW-DatabazovyServer (new)", "TS-NotifikacnaSluzba (unchanged)"]
  work_packages_deliverables: ["WP-004", "D-005 (new)", "D-009 (new)"]
  decisions: ["ADR-001", "ADR-002", "ADR-003", "ADR-004"]
  scenarios: ["SC-002-01", "SC-002-02", "SC-002-03", "SC-002-04", "SC-002-05", "SC-002-06", "SC-002-07", "SC-002-08"]
  tests: []
open_questions: ["Q-01", "Q-03", "Q-04b", "Q-05", "Q-06", "Q-07", "Q-08", "Q-09", "Q-10b", "Q-11", "Q-13"]
```

## Navrhovaný výstup

Drafty všetkých súborov registrovaných v spec/manifest.yaml (authoritative časť so stavom `draft`), ID mapovanie
v architecture-context.yaml, ADR-001…004 (Proposed), prompty v1.0.

## Validation results

Výsledok automatickej kontroly (syntax YAML, existencia IDs) je v `reports/2026-11-21-spec-check.txt`.

## Traceability summary

G-002 → R-002 → BS-VybavovanieTicketov → BP-VybavovanieTicketu → AS-SpravaTicketov → AC-MobilnaBrana → DO-Ticket →
US-002 → SC-002-01…08. Contract → code → test: čaká na Gate 6.

## Decision required / ADR

DECISION REQUIRED: Q-01, Q-03, Q-04b, Q-05, Q-06, Q-07, Q-08 (formát podľa AGENTS.md kap. 6 je v open-questions.md).
ADR na rozhodnutie: ADR-001, ADR-002, ADR-003, ADR-004.
**DESIGN_CONTRACT sa nesmie spustiť, kým nie sú tieto otázky uzavreté a ADR-001, ADR-002 prijaté.**

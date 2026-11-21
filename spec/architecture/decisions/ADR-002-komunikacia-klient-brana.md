# ADR-002 Komunikačný štýl medzi klientom a Mobilnou bránou pre tickety

## Status
Accepted

## Context
INT-001 (Manažment ticketov → Mobilná brána) a INT-002 (klient posudzovateľa → Mobilná brána) používajú AS-SpravaTicketov
cez AIF-APIBrany. Model obsahuje princíp PRI-003 „otvorené rozhrania REST / HTTPS + JSON“, ale poznámka pri ňom uvádza,
že protokol rozhraní API brány nie je v modeli uvedený („OVERIŤ“). AI nesmie sama rozhodnúť sync API verzus event. Otázka Q-13.

## Options
1. **Synchronné HTTP API (REST / HTTPS + JSON).** Používateľ dostane výsledok operácie hneď (prijatý / odmietnutý ticket,
   výsledok rozhodnutia). Zodpovedá PRI-003 a existujúcemu AIF-APIBrany. Contract v OpenAPI.
2. **Asynchrónne udalosti.** Klient odošle požiadavku a výsledok dostane neskôr; potrebuje broker, ktorý v modeli nie je.

## Decision
Zvolená možnosť 1 (synchrónne REST / HTTPS + JSON) – rozhodla Anna-Mariia Malesh, 2026-11-21 (Q-13). Stav Accepted zapíše človek. Notifikácie o výsledku (INT-003) sú samostatná
asynchrónna časť – pozri ADR-003.

## Consequences
- Contract bude OpenAPI 3.1 podľa spec/policies/contract-design-profile.yaml.
- Chyby sa vracajú hneď v odpovedi (problem details).
- Nevzniká závislosť na message brokeri.

## Related elements
R-002, INT-001, INT-002, AIF-APIBrany, AS-SpravaTicketov, AC-MobilnaBrana, PRI-003

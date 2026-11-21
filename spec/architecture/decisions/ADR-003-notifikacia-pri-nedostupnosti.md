# ADR-003 Oznámenie výsledku ticketu a nedostupnosť notifikačnej služby

## Status
Accepted

## Context
BP-PosudenieTicketu spúšťa BP-OznamenieVysledku, ktorý podporuje AS-Notifikacie. Notifikácie doručuje externá
TS-NotifikacnaSluzba (NODE-FCM). Specification neurčuje, pri ktorých zmenách stavu sa notifikácia posiela, ani čo sa stane,
keď je služba nedostupná. Otázka Q-07; pravidlo BR-007; QR-003.

## Options
1. **Rozhodnutie sa uloží vždy, notifikácia je best-effort.** Zlyhanie odoslania sa zaznamená; žiadateľ výsledok vidí v aplikácii.
2. **Rozhodnutie sa uloží vždy, zlyhaná notifikácia sa automaticky opakuje.** Potrebuje frontu a pravidlá opakovania.
3. **Rozhodnutie sa neuloží, ak notifikáciu nemožno odoslať.** Posudzovateľ musí rozhodnutie zopakovať.

Rozsah notifikácií: A) pri prevzatí aj pri rozhodnutí, B) iba pri rozhodnutí.

## Decision
Zvolená možnosť 1 a rozsah B: notifikácia iba pri rozhodnutí, rozhodnutie sa uloží vždy, zlyhanie notifikácie sa
zaznamená – rozhodla Anna-Mariia Malesh, 2026-11-21 (Q-07). Stav Accepted zapíše človek.

## Consequences
- Contract nevracia chybu posudzovateľovi kvôli nedostupnej notifikačnej službe.
- Implementácia oddelí uloženie stavu od odoslania notifikácie; v testoch sa notifikačná služba nahradí testovacou náhradou.
- Notifikácia neobsahuje osobné údaje, iba identifikátor ticketu a stav (QR-004).

## Related elements
R-002, BR-007, QR-003, QR-004, AS-Notifikacie, AF-OdosielanieNotifikacii, TS-NotifikacnaSluzba, NODE-FCM, INT-003,
BP-OznamenieVysledku, REP-NotifikaciaStavuTicketu, GAP-003, D-009

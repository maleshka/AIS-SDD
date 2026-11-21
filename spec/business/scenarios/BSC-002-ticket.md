# BSC-002 Business Scenario – Vybavenie požiadavky ticketom

Stav: **approved** (Anna-Mariia Malesh, 2026-11-21) · Requirement: R-002 · Goal: G-002 · Baseline: B-01

## Problém (bez technológie)

Študent dnes rieši požiadavky na vyučujúceho alebo študijné oddelenie e-mailom alebo osobne.
Požiadavka nie je nikde evidovaná a študent nevie, v akom stave je jej vybavenie (DRV-001, ASM-003).

## Kto začne situáciu

Študent v roli **Žiadateľ** (ROLE-Ziadatel) má požiadavku alebo problém (BE-PoziadavkaStudenta),
napríklad potrebuje súhlas vyučujúceho alebo potvrdenie zo študijného oddelenia.

## Čo sa stane

1. Študent v aplikácii Moje štúdium vytvorí ticket: čo potrebuje, popis a komu je určený.
2. Ticket dostane jeho **Posudzovateľ** (ROLE-Posudzovatel) – vyučujúci alebo zamestnanec študijného oddelenia.
3. Posudzovateľ ticket prevezme a študent vidí, že sa na ňom pracuje.
4. Posudzovateľ ticket schváli alebo zamietne a pri zamietnutí uvedie dôvod.
5. Študent dostane oznámenie o výsledku a výsledok vidí aj v aplikácii.

## Očakávaný výsledok

Študent má požiadavku evidovanú na jednom mieste (PRI-001), vie, kto o nej rozhoduje, a pozná výsledok (OUT-002).

## Hranica riešenia

| V riešení | Mimo riešenia |
|---|---|
| Moje štúdium – modul Manažment ticketov (klient) | UIS (ticket sa v UIS neukladá) |
| Mobilná brána – evidencia ticketov, API brány, databáza brány | Klient pre posudzovateľa (používa API brány) |
| Notifikácie o výsledku (cez notifikačnú službu) | Firebase Cloud Messaging ako externá služba |
| | AS-IS postup e-mailom / osobne (ostáva ako alternatíva) |

## Rozhodnutia

Q-01, Q-03, Q-04b, Q-05, Q-06, Q-07, Q-08 rozhodla Anna-Mariia Malesh, 2026-11-21 – pozri [open-questions.md](../../drafts/open-questions.md).

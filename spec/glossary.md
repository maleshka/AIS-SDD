# Glossary – Moje štúdium extension (výrez R-002)

Každý pojem má jednu definíciu. Glossary neobsahuje názvy tried, tabuliek ani endpointov.

## Ticket

Štruktúrovaná žiadosť študenta, o ktorej rozhoduje vyučujúci alebo študijné oddelenie (MEA-Ticket). Má stav, ktorý študent môže sledovať.

- IDs: BO-Ticket, DO-Ticket
- Nepoužívať ako synonymum: Žiadosť (e-mail / osobne) – to je neštruktúrovaná AS-IS požiadavka bez stavu.

## Žiadateľ

Rola študenta, ktorý ticket vytvára a sleduje jeho vybavenie.

- IDs: ROLE-Ziadatel (plní ju ACT-Student)

## Posudzovateľ žiadosti

Rola, ktorá ticket prevezme a rozhodne o ňom (schváli alebo zamietne).

- IDs: ROLE-Posudzovatel (plní ju ACT-PedagogickyZbor alebo ACT-ZamestnanecSO)
- Skrátene: posudzovateľ

## Adresát ticketu

Konkrétny vyučujúci alebo študijné oddelenie, ktorého študent zvolí pri vytvorení ticketu. Iba adresát ticket vidí a rozhoduje (Q-03).

## Stav ticketu

Fáza vybavovania ticketu: **Podaný**, **V posudzovaní**, **Schválený**, **Zamietnutý**.

- IDs: DO-Ticket (lifecycle v spec/application/lifecycles.yaml)
- Schválený a Zamietnutý sú **rozhodnuté** (konečné) stavy.

## Prevzatie ticketu

Okamih, keď posudzovateľ začne ticket posudzovať; ticket prejde zo stavu Podaný do V posudzovaní. Rozhodnúť možno iba prevzatý ticket (Q-04b).

## Rozhodnutie o tickete

Schválenie alebo zamietnutie ticketu posudzovateľom, prípadne s odôvodnením.

## Odôvodnenie

Text posudzovateľa, ktorý vysvetľuje rozhodnutie. Povinný pri zamietnutí, voliteľný pri schválení (Q-06).

## Notifikácia o stave ticketu

Oznámenie doručené žiadateľovi na mobilné zariadenie o zmene stavu jeho ticketu.

- IDs: REP-NotifikaciaStavuTicketu, DO-Notifikacia, AS-Notifikacie

## Mobilná brána

Existujúca backendová časť riešenia, cez ktorú aplikácia Moje štúdium pristupuje k dátam a službám (klient – API – backend).

- IDs: AC-MobilnaBrana, AIF-APIBrany
- Nepoužívať ako synonymum: UIS

## UIS

Univerzitný informačný systém – externý systém, nie súčasť riešenia R-002. Ticket sa v UIS neukladá.

- IDs: AC-UIS

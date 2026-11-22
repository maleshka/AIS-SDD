# GAP Analysis

Status: **PERFORMED IN MODEL – APPROVED BY TEAM** (Anna-Mariia Malesh, 2026-11-22, Q-16)

Gaps sú spracované v modeli B-01 (diagram *Gap Analysis*, prvky Gap s typom zmeny v poznámke).
GAP Analysis je spracovaná v modeli a schválená tímom. AI nové gaps ani requirements z rozdielov nevytvára.

Porovnávané Plateaus:

- AS-IS: PL-ASIS (Súčasný stav)
- Prechod: PL-MVP (Prechodný stav (MVP))
- TO-BE: PL-TOBE (Cieľový stav)

## Gaps z modelu

| ID | Gap | Typ (z modelu) | Plateaus | Deliverable | Requirement |
|---|---|---|---|---|---|
| GAP-001 | Chýbajúci zápis do UIS cez mobilnú bránu | ZMENA (Mobilná brána) + NOVÉ (Databáza mobilnej brány, Databázový server) | ASIS → MVP | Rozšírená mobilná brána (zápisové API do UIS) | – |
| GAP-002 | Chýbajúce prijímanie a odosielanie správ v aplikácii | NOVÉ | ASIS → MVP | Modul správ | R-001 |
| GAP-003 | Chýbajúce notifikácie pre nové funkcie | ZMENA (Notifikácie) | ASIS → MVP → TOBE | Rozšírenie notifikácií, nové správy; **D-009** | R-001, **R-002**, R-005 |
| **GAP-004** | **Chýbajúca správa ticketov** | **NOVÉ** | MVP → TOBE | **D-005 Modul ticketov** | **R-002** |
| GAP-005 | Chýbajúce prihlasovanie na témy | NOVÉ (aplikačná služba) | MVP → TOBE | Modul prihlasovania na témy | R-003 |
| GAP-006 | Chýbajúce odovzdanie zadaní | NOVÉ (aplikačná služba) | MVP → TOBE | Modul odovzdania zadaní | R-004 |
| GAP-007 | Chýbajúca rezervácia miestností | NOVÉ (modul) + ZMENA (Workzone) | MVP → TOBE | Modul rezervácií (zápis do Workzone) | R-005 |

## GAP-004 – detail pre R-002 (z poznámky v modeli)

Rozdiel: požiadavky sa vybavujú e-mailom alebo osobne, bez evidencie a sledovania stavu.
TO-BE: ticket so stavom a notifikáciou ako nová možnosť; o tickete rozhoduje vyučujúci alebo študijné oddelenie.
E-mailový a osobný postup ostáva ako alternatíva. Ticket sa ukladá v databáze mobilnej brány. Typ: NOVÉ.

Dotknuté prvky (väzby Association v modeli): R-002, AS-SpravaTicketov, BP-VybavovanieTicketu,
BP-ASIS-VybaveniePoziadavky, PL-MVP, PL-TOBE, D-005.

## Obrázok

`spec/architecture/views/B-01-gap-analysis.jpg` – diagram je usporiadaný ako matica
AS-IS (baseline) → GAP → TO-BE (target) → Požiadavka → Deliverable. Pre GAP-004: AS-IS *Vybavenie požiadavky na študijnom
oddelení* → GAP *Chýbajúca správa ticketov* → TO-BE *Vybavovanie ticketu*, *Správa ticketov* → R-002 → D-005.

## Čo chýba

- Explicitné označenie ZHODA / ZMENA / NOVÉ / ODSTRÁNENÉ priamo v matici (typ je zatiaľ iba v poznámkach prvkov Gap).

Nevyriešený gap blokuje iba zmenu, ktorá od neho závisí. R-002 má vlastný Requirement, preto ho neblokuje.

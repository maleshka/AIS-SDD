# ADR-001 Hranica služby Správa ticketov a vlastník DO-Ticket

## Status
Accepted

## Context
V modeli B-01 realizujú AS-SpravaTicketov dva prvky: AC-ManazmentTicketov, ktorý je vnorený v klientovi AC-MojeStudium,
a AF-EvidenciaTicketov, priradená AC-MobilnaBrana. DO-Ticket pristupuje iba AC-MobilnaBrana a ticket realizuje
ART-DatabazaMobilnejBrany na serveri mobilnej brány. Princíp PRI-002 požaduje oddelenie klienta od biznis logiky.
Bez jednoznačného poskytovateľa nemožno navrhnúť contract (Gate 3). Otázka Q-01.

## Options
1. **AC-MobilnaBrana poskytuje AS-SpravaTicketov cez AIF-APIBrany a vlastní DO-Ticket.** AC-ManazmentTicketov je klientský
   modul Moje štúdium, ktorý službu iba používa. Model netreba meniť, iba spresniť význam väzby Realization.
2. **AC-ManazmentTicketov je samostatný backendový komponent.** Vyžaduje presunúť ho z Moje štúdium, doplniť nové rozhranie
   a nový deployment; je v rozpore s umiestnením databázy.

## Decision
Zvolená možnosť 1 – rozhodla Anna-Mariia Malesh, 2026-11-21 (Q-01). Stav Accepted zapíše človek.

## Consequences
- Contract API-Tickets bude rozhraním AIF-APIBrany poskytovaným AC-MobilnaBrana.
- Pravidlá BR-001 až BR-007 sa vynucujú v Mobilnej bráne, nie v klientovi.
- Klient ani iný komponent nesmie meniť DO-Ticket obídením API brány.
- Odporúča sa v Sparx EA doplniť poznámku k AC-ManazmentTicketov („klientský modul“).

## Related elements
R-002, AS-SpravaTicketov, AC-MobilnaBrana, AC-ManazmentTicketov, AC-MojeStudium, AF-EvidenciaTicketov, AIF-APIBrany,
DO-Ticket, ART-DatabazaMobilnejBrany, PRI-002

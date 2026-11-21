# ADR-004 Technológia candidate code pre Mobilnú bránu (výrez R-002)

## Status
Accepted

> Voľbu urobil autor projektu 2026-11-21 (odpoveď na otázku AI: „Python + FastAPI + SQLite/PostgreSQL“).
> Stav **Accepted** nastaví človek pri review; AI ho nastaviť nesmie.

## Context
Model B-01 uvádza iba všeobecné SSW-AplikacnyServer a SSW-DatabazovyServer na NODE-ServerMobilnejBrany, bez produktu.
Na vygenerovanie candidate code a testov (etapa 7) treba zvoliť jazyk, framework a spôsob ukladania DO-Ticket.
AI nesmie produkt zvoliť sama (AGENTS.md, kap. 5).

## Options
1. **Python 3 + FastAPI**, ukladanie v relačnej databáze; v testoch SQLite (bez inštalácie DBMS). Najmenej kódu, OpenAPI
   sa dá porovnať s approved contractom automaticky, testy v pytest.
2. **Java + Spring Boot** – viac kódu, potrebuje JDK a build nástroj.
3. **Node.js + Express** – testy v Jest.

## Decision
Zvolená možnosť 1 – rozhodla Anna-Mariia Malesh, 2026-11-21 (Q-14a). Stav Accepted zapíše človek.

Otvorené: konkrétny DBMS pre prevádzku (PostgreSQL je kandidát, nie rozhodnutie) a verzie – doplní človek pred nasadením.

## Consequences
- src/ obsahuje Python balík backendu Mobilnej brány pre AS-SpravaTicketov.
- SSW-AplikacnyServer = Python runtime + ASGI server; SSW-DatabazovyServer = relačný DBMS.
- Notifikačná služba (NODE-FCM) sa v testoch nahradí testovacou náhradou cez rozhranie odosielania notifikácií.
- Nová závislosť: FastAPI, pydantic, ASGI server; testy: pytest, httpx.

## Related elements
SSW-AplikacnyServer, SSW-DatabazovyServer, NODE-ServerMobilnejBrany, ART-BackendMobilnejBrany, ART-DatabazaMobilnejBrany,
AC-MobilnaBrana, R-002

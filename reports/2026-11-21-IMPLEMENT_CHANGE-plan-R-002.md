# IMPLEMENT_CHANGE – generation plan R-002

Dátum: 2026-11-21 · Prompt: spec/prompts/implement-change.md v1.0 · Approved contract: **API-Tickets 0.1.0**
(spec/contracts/approved/, approval.yaml – Anna-Mariia Malesh) · Specification 0.2.1 · Baseline B-01

## Kontrola vstupov

| Vstup | Stav |
|---|---|
| Approved contract a approval.yaml | ✅ API-Tickets 0.1.0 |
| Application Structure / Cooperation / Usage / Service Realization | ✅ approved; kód vzniká iba v AC-MobilnaBrana (ADR-001) |
| ADR-001…004 | ✅ Accepted |
| Otvorené DECISION REQUIRED | žiadne |

## Hranice

- Kód realizuje **iba AC-MobilnaBrana** (ART-BackendMobilnejBrany). Klient AC-ManazmentTicketov sa negeneruje.
- Žiadna závislosť na AC-UIS (components.yaml `not_allowed_for_r002`).
- Notifikačná služba (TS-NotifikacnaSluzba / NODE-FCM) je za rozhraním `OdosielatelNotifikacii`; v testoch testovacia náhrada.
  Produkčný adaptér na FCM nie je súčasťou rozsahu.
- Overenie identity (Q-10a/b) je za rozhraním `OverovacIdentity`; produkčné napojenie na existujúce prihlásenie nie je
  súčasťou rozsahu, v testoch testovacie tokeny.
- Ukladanie DO-Ticket: relačná DB cez `sqlite3` zo štandardnej knižnice (ADR-004 – SQLite v testoch). Nejde o databázový
  návrh pre prevádzku.

## Súbory

| Súbor | Obsah | Väzby |
|---|---|---|
| `src/mobilna_brana/identity.py` | Používateľ, role, rozhranie overenia tokenu | QR-001, Q-10a/b |
| `src/mobilna_brana/notifikacie.py` | Rozhranie odosielania notifikácie (iba ticketId + stav) | AS-Notifikacie, INT-003, QR-004 |
| `src/mobilna_brana/tickety/uloziste.py` | Uloženie ticketov, audit, idempotency kľúče; atómové prechody stavu | DO-Ticket, QR-002, BR-001, Q-11 |
| `src/mobilna_brana/tickety/sluzba.py` | Pravidlá BR-001…BR-007 a lifecycle | AS-SpravaTicketov, AF-EvidenciaTicketov |
| `src/mobilna_brana/api.py` | FastAPI aplikácia podľa API-Tickets 0.1.0, problem+json | AIF-APIBrany |
| `tests/test_akceptacia.py` | Acceptance testy SC-002-01…SC-002-11 + invarianty BR-001, BR-003 | US-002.feature |
| `tests/test_contract.py` | Zhoda implementácie s approved OpenAPI | API-Tickets 0.1.0 |
| `tests/conftest.py` | Klient, testovacie tokeny, testovacia náhrada notifikácií, kontrola každej odpovede voči contractu | – |
| `requirements.txt`, `pytest.ini` | Závislosti a nastavenie testov | ADR-004 |

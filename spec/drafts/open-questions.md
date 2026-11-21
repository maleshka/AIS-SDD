# Otvorené otázky a rozhodnutia – R-002 Ticket

Specification baseline: 0.2.1 (approved) · Architecture baseline: B-01

Rozhodnutia urobil človek (odpovede na otázky AI v konverzácii). AI ich iba zapísala na miesta uvedené v stĺpci „Zapísané v“.
Stav súborov (`draft` → `approved`) a ADR (`Proposed` → `Accepted`) mení človek pri review.

## Rozhodnuté

| ID | Otázka | Rozhodnutie | Rozhodol/a, dátum | Zapísané v |
|---|---|---|---|---|
| Q-01 | Kto poskytuje AS-SpravaTicketov a vlastní DO-Ticket | **Mobilná brána** (cez AF-EvidenciaTicketov a AIF-APIBrany); AC-ManazmentTicketov je klientský modul Moje štúdium | Anna-Mariia Malesh, 2026-11-21 | ADR-001, components.yaml, data-objects.yaml, service-realization.yaml |
| Q-02 | Kde rozhoduje posudzovateľ | Cez API mobilnej brány; klient pre zamestnancov je mimo rozsahu | Anna-Mariia Malesh, 2026-11-21 | interactions.yaml INT-002, BR-002 |
| Q-03 | Kto posudzuje a vidí konkrétny ticket | **Adresát zvolený študentom** (konkrétny vyučujúci alebo študijné oddelenie – vtedy ktorýkoľvek zamestnanec ŠO) | Anna-Mariia Malesh, 2026-11-21 | BR-002, BR-003, glossary |
| Q-04a | Stavy ticketu | Podaný → V posudzovaní → Schválený / Zamietnutý; rozhodnutý ticket je konečný | Anna-Mariia Malesh, 2026-11-21 | lifecycles.yaml, BR-001 |
| Q-04b | Prechod Podaný → V posudzovaní | **Posudzovateľ ticket prevezme**; rozhodnúť možno iba ticket V posudzovaní | Anna-Mariia Malesh, 2026-11-21 | lifecycles.yaml, BR-004 |
| Q-05 | Povinné údaje ticketu | **Predmet, popis, adresát**; bez príloh | Anna-Mariia Malesh, 2026-11-21 | BR-005, data-objects.yaml, SC-002-02 |
| Q-06 | Odôvodnenie rozhodnutia | **Povinné pri zamietnutí**, voliteľné pri schválení | Anna-Mariia Malesh, 2026-11-21 | BR-006, SC-002-06, SC-002-09 |
| Q-07 | Notifikácie a výpadok notifikačnej služby | **Iba pri rozhodnutí**; rozhodnutie sa uloží vždy, zlyhanie notifikácie sa zaznamená | Anna-Mariia Malesh, 2026-11-21 | ADR-003, BR-007, QR-003, INT-003, SC-002-11 |
| Q-08 | Prístup a audit (GDPR) | Ticket vidí **iba žiadateľ a adresát**; každá zmena stavu sa **auditne zaznamená** | Anna-Mariia Malesh, 2026-11-21 | BR-003, QR-002, SC-002-04 |
| Q-10a | Autentifikácia | Existujúce prihlásenie aplikácie, bearer token | Anna-Mariia Malesh, 2026-11-21 | contract-design-profile.yaml, QR-001 |
| Q-10b | Odkiaľ brána pozná rolu | Identitu a rolu dodá existujúce prihlásenie; v testoch testovací token | Anna-Mariia Malesh, 2026-11-21 | contract-design-profile.yaml, QR-001 |
| Q-11 | Opakované odoslanie a súbeh | **Ochrana proti duplicite** (`Idempotency-Key` pri vytvorení); pri súbehu rozhodnutí platí prvé (BR-001) | Anna-Mariia Malesh, 2026-11-21 | contract-design-profile.yaml, BR-001, SC-002-10 |
| Q-19 | Kto rozhoduje prevzatý ticket (najmä pri adresátovi ŠO) | **Iba posudzovateľ, ktorý ticket prevzal**; iný ho už prevziať ani rozhodnúť nemôže | Anna-Mariia Malesh, 2026-11-21 | BR-004 (0.2.1), API-Tickets rozhodnutTicket |
| Q-13 | Komunikačný štýl klient ↔ brána | **Synchrónne REST / HTTPS + JSON** | Anna-Mariia Malesh, 2026-11-21 | ADR-002, interactions.yaml |
| Q-14a | Technológia candidate code | Python + FastAPI, relačná DB (SQLite v testoch) | Anna-Mariia Malesh, 2026-11-21 | ADR-004 |

## Stále otvorené (neblokujú návrh contractu)

### 🟡 Q-09 Deployment väzba v modeli
V modeli chýba `ART-BackendMobilnejBrany —Realization→ AC-MobilnaBrana`. Doplniť v Sparx EA alebo potvrdiť ako známu medzeru.
Kam zapísať: deployment.yaml · Rozhodnutie: ___

### 🟡 Q-18 Vlastníci requirementu, constraintu a quality requirements
`owner: null` je pri C-001, BR-003 a QR-001…QR-004 – model vlastníka neurčuje. Doplní človek (napr. rola „Zodpovedná osoba GDPR“
alebo „Študijné oddelenie“). Zároveň potvrdiť QR-004 (osobné údaje nie sú v logu ani v push notifikácii) – odvodené z C-001, nebolo
výslovne rozhodnuté.

### ⚪ Q-15 Čísla kvality
Čas odpovede, dostupnosť, RTO/RPO nie sú v podkladoch určené. Nevypĺňajú sa odhadom.

### ⚪ Q-16 Stav GAP Analysis
Gaps sú v modeli spracované (matica AS-IS → GAP → TO-BE). Treba potvrdiť, či je GAP Analysis schválená.

### ⚪ Q-17 Enterprise Continuum – vlastník, verzia, zrelosť
Pri ABB aj SBB sú tieto údaje väčšinou UNKNOWN. Pre R-002 sa reuse nemení, ale katalóg nesmie uvádzať reuse ako schválený bez nich.

### ⚪ Doba uchovávania ticketov
Nie je v modeli ani v podkladoch; doplní vlastník (napr. podľa DPIA v D-001).

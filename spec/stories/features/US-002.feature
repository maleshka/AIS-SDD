# language: sk
# Stav: approved (Anna-Mariia Malesh, 2026-11-21). Rozhodnutia Q-03…Q-08: Anna-Mariia Malesh, 2026-11-21.

Požiadavka: Vytvorenie a sledovanie ticketu
  Ako študent chcem vytvoriť ticket a sledovať jeho schválenie alebo zamietnutie.

  @SC-002-01 @R-002 @BR-005
  Scenár: Študent podá úplný ticket
    Pokiaľ študent je prihlásený v aplikácii
    Keď študent podá ticket s predmetom, popisom a adresátom
    Potom ticket je evidovaný v stave Podaný
    A študent ho vidí medzi svojimi ticketmi

  @SC-002-02 @R-002 @BR-005
  Scenár: Neúplný ticket sa nepodá
    Pokiaľ študent je prihlásený v aplikácii
    Keď študent podá ticket bez popisu požiadavky
    Potom systém ticket neprijme
    A oznámi, ktorý údaj chýba

  @SC-002-03 @R-002
  Scenár: Študent sleduje stav svojho ticketu
    Pokiaľ študent má ticket, ktorý posudzovateľ prevzal
    Keď si študent zobrazí svoj ticket
    Potom vidí stav V posudzovaní

  @SC-002-04 @R-002 @BR-003 @C-001
  Scenár: Študent nevidí cudzí ticket
    Pokiaľ existuje ticket iného študenta
    Keď si študent vyžiada tento ticket
    Potom systém mu ticket nesprístupní

  @SC-002-05 @R-002 @BR-004 @BR-007
  Scenár: Posudzovateľ schváli ticket
    Pokiaľ ticket je V posudzovaní u svojho adresáta
    Keď posudzovateľ ticket schváli
    Potom ticket je v stave Schválený
    A žiadateľ dostane oznámenie o výsledku

  @SC-002-06 @R-002 @BR-006 @BR-007
  Scenár: Posudzovateľ zamietne ticket s odôvodnením
    Pokiaľ ticket je V posudzovaní u svojho adresáta
    Keď posudzovateľ ticket zamietne s odôvodnením
    Potom ticket je v stave Zamietnutý
    A žiadateľ vidí odôvodnenie
    A žiadateľ dostane oznámenie o výsledku

  @SC-002-07 @R-002 @BR-001
  Scenár: Rozhodnutý ticket sa nedá znovu rozhodnúť
    Pokiaľ ticket je v stave Schválený
    Keď posudzovateľ sa pokúsi ticket zamietnuť
    Potom systém zmenu odmietne
    A ticket ostane v stave Schválený

  @SC-002-08 @R-002 @BR-002
  Scenár: Žiadateľ nemôže rozhodnúť o svojom tickete
    Pokiaľ študent má ticket v stave V posudzovaní
    Keď študent sa pokúsi svoj ticket schváliť
    Potom systém zmenu odmietne
    A ticket ostane v stave V posudzovaní

  @SC-002-09 @R-002 @BR-006
  Scenár: Zamietnutie bez odôvodnenia sa neprijme
    Pokiaľ ticket je V posudzovaní u svojho adresáta
    Keď posudzovateľ ticket zamietne bez odôvodnenia
    Potom systém zamietnutie neprijme
    A ticket ostane v stave V posudzovaní

  @SC-002-10 @R-002 @BR-005
  Scenár: Opakované odoslanie toho istého ticketu nevytvorí druhý ticket
    Pokiaľ študent podal ticket a odoslanie zopakoval s rovnakým kľúčom požiadavky
    Keď systém prijme opakované odoslanie
    Potom študent má evidovaný iba jeden takýto ticket

  @SC-002-11 @R-002 @BR-007
  Scenár: Výpadok notifikácií nezruší rozhodnutie
    Pokiaľ ticket je V posudzovaní u svojho adresáta
    A notifikačná služba je nedostupná
    Keď posudzovateľ ticket schváli
    Potom ticket je v stave Schválený
    A žiadateľ vidí výsledok pri sledovaní ticketu

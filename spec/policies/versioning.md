# Pravidlá verziovania (G0 Framework ready)

Stav: **draft** – schvaľuje človek (Solution Architect). Do schválenia ide iba o návrh.

## Čo má verziu

| Prvok | Kde je verzia | Formát |
|---|---|---|
| Specification package | `spec/manifest.yaml` → `specification.version` | MAJOR.MINOR.PATCH |
| Architektonický model | `spec/manifest.yaml` → `architecture_baseline` + názov .qea súboru | B-01, B-02 … |
| Requirement, pravidlo (BR) | pole `version` v zázname | MAJOR.MINOR |
| Contract | `info.version` v OpenAPI + `approval.yaml` | MAJOR.MINOR.PATCH |
| ADR | nová verzia = nové ADR, staré dostane stav Superseded | ADR-xxx |
| Prompt | nadpis súboru v `spec/prompts/` | vMAJOR.MINOR |
| Generovaný kód a testy | hlavička súboru (specification, contract, baseline, prompt) | – |

## Kedy sa zvyšuje verzia špecifikácie

| Zmena | Verzia | Príklad |
|---|---|---|
| Mení sa cieľ, ruší sa alebo zásadne mení requirement, mení sa hranica komponentu | **MAJOR** | ticket sa presunie do UIS |
| Nový requirement, nový scenár, nové pravidlo, nový stav v lifecycle | **MINOR** | študent môže stiahnuť ticket |
| Spresnenie nejednoznačnosti rozhodnutím (DECISION REQUIRED) bez zmeny schválených scenárov | **PATCH** | 0.2.0 → 0.2.1 (Q-19) |

## Kedy sa zvyšuje verzia contractu

| Zmena | Verzia |
|---|---|
| Odstránená alebo premenovaná operácia či pole, nové povinné pole, zmenený význam status kódu (breaking) | **MAJOR** – vyžaduje ľudské rozhodnutie o kompatibilite |
| Nová operácia, nové voliteľné pole, nová hodnota enumu, ktorú starý klient môže ignorovať | **MINOR** |
| Iba opis, príklady, preklepy | **PATCH** |

Kým je contract vo verzii 0.x, MINOR môže obsahovať aj breaking zmenu, ale report DESIGN_CONTRACT ju musí výslovne uviesť.

## Baseline a zmeny v gite

1. Každá schválená verzia špecifikácie dostane tag `spec-v<verzia>` (napr. `spec-v0.2.1`).
2. Každá zmena (Change ID) má vlastnú vetvu `change/<Change ID>` a jeden pull request.
   Spolu sa mení requirement, model/views, ADR, contract, kód, testy a traceability.
3. PR sa zlúči až po ľudskom review; potom sa vytvorí nový tag baseline.
4. Approval záznamy (`approval.yaml`, `reviewed_by`, `approved_by`) obsahujú verziu a commit alebo PR.

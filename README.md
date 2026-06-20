# 🏆 Tipovačka MS 2026

Žebříček a statistiky naší tipovací soutěže na MS ve fotbale 2026.
Stránka: **https://m0xt.github.io/tipovacka-ms2026/**

## Jak to funguje

Stránka (`index.html`) čte data **živě z Google Sheetu** při každém načtení — není potřeba
nic přegenerovávat ani nasazovat. Sheet je jediný zdroj pravdy:

- **Tipy hráčů** (1 = výhra domácích, 0 = remíza, 2 = výhra hostů) a **tipy na vítěze** = ze sheetu
- **Výsledky** zadáváš ručně do sloupce **„Výsledek"** ve tvaru `2:0` (domácí:hosté)

Bodování: **1 bod** za trefený výsledek, **+5 bodů** za správně tipnutého vítěze turnaje
(přičte se po finále — nastav `ACTUAL_CHAMPION` v `index.html`).

## Zadávání výsledků

1. V Google Sheetu nech/přidej sloupec s hlavičkou **`Výsledek`**.
2. Naformátuj ho jako **Prostý text** (Formát → Číslo → Prostý text), ať Sheets nepřevádí `2:0` na čas.
3. Píš výsledky odehraných zápasů ve tvaru `2:0`. Neodehrané nech prázdné.
4. Stránka se aktualizuje sama (Google data publikuje s ~5min zpožděním; tlačítko „↻ obnovit" načte znovu).

Pozn.: tipy na vítěze jsou neměnné a Google CSV je z číselných sloupců nevyexportuje,
proto jsou pro jistotu zapečené v `index.html` (mapováno podle jména hráče).

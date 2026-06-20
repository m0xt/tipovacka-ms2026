# 🏆 Tipovačka MS 2026

Žebříček a statistiky naší tipovací soutěže na MS ve fotbale 2026.

- **Bodování:** 1 bod za správně tipnutý výsledek (1 = výhra domácích, 0 = remíza, 2 = výhra hostů), +5 bodů za správně tipnutého celkového vítěze turnaje (po finále).
- **Stránka:** statická, generovaná z tipů ze sdíleného Google Sheetu.

## Jak aktualizovat výsledky

1. Doplň/uprav výsledky v `results.json` ve formátu `"<číslo zápasu>": [góly_domácí, góly_hosté]`
2. Spusť `python3 build.py`
3. `git add -A && git commit -m "výsledky" && git push`

GitHub Pages se aktualizuje samo do pár minut. Výsledky se navíc dohledávají automaticky během dne.

Až bude znám vítěz turnaje, nastav v `build.py` v `CONFIG` hodnotu `"champion"` na vítězný tým.

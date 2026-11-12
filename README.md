# Tanulási napló

A Tanulási napló Pythonban készült asztali alkalmazás a tanulási alkalmak nyilvántartására és elemzésére.

## Funkciók

- Tanulási alkalmak rögzítése dátummal, tantárggyal, időtartammal és koncentrációval.
- Bejegyzések megjelenítése, tantárgy szerinti szűrése és törlése.
- Összes tanulási idő, átlag, medián és szórás számítása.
- Tantárgyankénti időráfordítás megjelenítése diagramon.
- Adatok automatikus mentése és betöltése JSON-fájlból.

## Indítás

Python 3 és Tkinter szükséges. A projekt a PyCharmban is megnyitható.

```bash
python main.py
```

## Fájlok

- `main.py` – grafikus felület és eseménykezelés.
- `aa_naplo.py` – bejegyzések kezelése, mentés és tantárgyi összesítés.
- `statisztika_bemutato.py` – átlag, medián és szórás számítása.
- `tesztek/test_naplo.py` – automatikus tesztek.

A bejegyzéseket a program a `tanulasi_adatok.json` fájlban tárolja.

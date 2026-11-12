Tanulási napló

Hallgató: Ács Adorján  
Monogram: AA

Feladat leírása

A Tanulási napló egy Pythonban készült grafikus alkalmazás, amely tanulási alkalmak nyilvántartására és statisztikai elemzésére szolgál.

A program lehetővé teszi a dátum, tantárgy, tanulási idő, koncentráció és megjegyzés rögzítését. A bejegyzések megtekinthetők, tantárgyanként szűrhetők és törölhetők.

Az alkalmazás kiszámítja az összes tanulási időt, az átlagot, a mediánt és a szórást. A tantárgyankénti időráfordítást diagramon jeleníti meg. Az adatokat automatikusan JSON-fájlba menti.

Modulok és függvények

main.py

A grafikus felület és az eseménykezelés megvalósítása a tkinter modul segítségével.

Főbb függvények és metódusok:
- main() – a program indítása.
- hozzaad() – új tanulási alkalom rögzítése.
- torol() – kiválasztott bejegyzés törlése.
- mintaadatok() – példaadatok betöltése.
- frissit( – a megjelenített adatok frissítése.
- statisztika_frissit() – statisztikai értékek frissítése.
- diagram_rajzol(` – diagram megjelenítése.

aa_naplo.py

Saját modul a tanulási alkalmak kezelésére és az adatok tárolására.

Függvények és metódusok:
- aa_tantargyi_osszesites() – tanulási idő összesítése tantárgyanként.
- betolt() – adatok betöltése.
- ment() – adatok mentése.
- ervenyes_bejegyzes() – adatok ellenőrzése.
- uj_bejegyzes() – új bejegyzés létrehozása.
- hozzaad() – bejegyzés hozzáadása.
- tobbet_hozzaad() – több bejegyzés hozzáadása.
- torol( – bejegyzés törlése.

statisztika_bemutato.py

Statisztikai számításokat végző modul, amely a Python statistics modulját használja.

Függvények:
- atlag_perc() – átlagos tanulási idő számítása a statistics.mean() függvénnyel.
- median_perc() – medián számítása a statistics.median() függvénnyel.
- szoras_perc() – szórás számítása a statistics.pstdev() függvénnyel.
- bemutato() – a statisztikai függvények bemutatása.

Felhasznált Python-modulok

- tkinter – grafikus felület és eseménykezelés.
- statistics – statisztikai számítások.
- json – adatok mentése és betöltése.
- datetime – dátumok kezelése.
- pathlib – fájlelérési utak kezelése.
- uuid – egyedi bejegyzésazonosítók létrehozása.

Osztályok

AANaplo

A tanulási bejegyzések tárolását, ellenőrzését, hozzáadását, törlését és mentését végző saját osztály.

AATanulasiAlkalmazas

A grafikus felületet, a felhasználói eseményeket, az adattáblázatot és a statisztikai diagramot kezelő osztály.

Program indítása

A program Python 3 és Tkinter használatával futtatható. A projekt PyCharmban is megnyitható.


python main.py


A tanulási adatokat az alkalmazás a tanulasi_adatok.jso fájlban tárolja.

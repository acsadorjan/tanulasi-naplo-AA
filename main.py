import tkinter as tk
from datetime import date, datetime, timedelta
from pathlib import Path
from tkinter import messagebox, ttk

from aa_naplo import AANaplo, aa_tantargyi_osszesites
from statisztika_bemutato import atlag_perc, median_perc, szoras_perc


ADATFAJL = Path(__file__).resolve().parent / "tanulasi_adatok.json"
HATTER = "#f3f6fb"
KARTYA = "#ffffff"
SOTET = "#16243a"
MASODLAGOS = "#526279"
KEK = "#2864dc"
ZOLD = "#17897c"
SZURO_MIND = "Összes tantárgy"
TANTARGYAK = (
    "Programozás",
    "Matematika",
    "Angol",
    "Fizika",
    "Történelem",
    "Egyéb",
)


class AATanulasiAlkalmazas:
    def __init__(self, root):
        self.root = root
        self.naplo = AANaplo(ADATFAJL)
        self.datum = tk.StringVar(value=date.today().isoformat())
        self.tantargy = tk.StringVar(value=TANTARGYAK[0])
        self.perc = tk.StringVar(value="45")
        self.fokusz = tk.StringVar(value="4")
        self.megjegyzes = tk.StringVar()
        self.szuro = tk.StringVar(value=SZURO_MIND)
        self.kijelolt_azonosito = None
        self.kartyak = {}

        self.root.title("Tanulási napló | Statisztikai elemző")
        self.root.geometry("1120x760")
        self.root.minsize(900, 680)
        self.root.configure(bg=HATTER)

        self.stilusok()
        self.felulet()
        self.frissit()

    def stilusok(self):
        stilus = ttk.Style(self.root)
        stilus.theme_use("clam")
        stilus.configure("TFrame", background=HATTER)
        stilus.configure("TEntry", padding=4, font=("Segoe UI", 10))
        stilus.configure("TCombobox", padding=4, font=("Segoe UI", 10))
        stilus.configure(
            "Main.TButton",
            padding=(12, 8),
            background=KEK,
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
        )
        stilus.map("Main.TButton", background=[("active", "#1f4caa")])
        stilus.configure(
            "Alt.TButton", padding=(10, 6), font=("Segoe UI", 10)
        )
        stilus.configure(
            "Danger.TButton", padding=(11, 8), font=("Segoe UI", 10)
        )
        stilus.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=29,
            background=KARTYA,
            fieldbackground=KARTYA,
            foreground=SOTET,
        )
        stilus.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#edf2f9",
            foreground=SOTET,
            padding=8,
        )
        stilus.map(
            "Treeview",
            background=[("selected", "#dce9ff")],
            foreground=[("selected", SOTET)],
        )

    def felulet(self):
        kulso = tk.Frame(self.root, bg=HATTER, padx=24, pady=13)
        kulso.pack(fill="both", expand=True)

        self.fejlec_letrehoz(kulso)
        self.kartyak_letrehoz(kulso)

        torzs = tk.Frame(kulso, bg=HATTER)
        torzs.pack(fill="both", expand=True)
        torzs.grid_columnconfigure(0, minsize=295, weight=0)
        torzs.grid_columnconfigure(1, weight=1)
        torzs.grid_rowconfigure(0, weight=1)

        self.bevitel_letrehoz(torzs)
        self.adatok_letrehoz(torzs)
        self.root.bind("<Control-Return>", self.hozzaad)

    def fejlec_letrehoz(self, szulo):
        tk.Label(
            szulo,
            text="TANULÁSI NAPLÓ",
            font=("Segoe UI", 10, "bold"),
            fg=KEK,
            bg=HATTER,
        ).pack(anchor="w")
        tk.Label(
            szulo,
            text="Lásd, mire fordítod az idődet!",
            font=("Segoe UI", 22, "bold"),
            fg=SOTET,
            bg=HATTER,
        ).pack(anchor="w", pady=(2, 2))
        tk.Label(
            szulo,
            text="Rögzíts tanulási alkalmakat, kövesd a tantárgyaidat, "
                 "és elemezd az eredményeidet.",
            font=("Segoe UI", 10),
            fg=MASODLAGOS,
            bg=HATTER,
        ).pack(anchor="w", pady=(0, 9))

    def kartyak_letrehoz(self, szulo):
        mutatok = tk.Frame(szulo, bg=HATTER)
        mutatok.pack(fill="x", pady=(0, 11))
        mutatok_adatok = (
            ("ÖSSZES TANULÁSI IDŐ", "osszes"),
            ("ÁTLAG / ALKALOM", "atlag"),
            ("MEDIÁN", "median"),
            ("SZÓRÁS", "szoras"),
        )
        for cim, kulcs in mutatok_adatok:
            kartya = self.kartya(mutatok, padx=16, pady=9)
            kartya.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 10) if kulcs != "szoras" else 0,
            )
            tk.Label(
                kartya,
                text=cim,
                font=("Segoe UI", 9, "bold"),
                fg=MASODLAGOS,
                bg=KARTYA,
            ).pack(anchor="w")
            ertek = tk.Label(
                kartya,
                text="–",
                font=("Segoe UI", 17, "bold"),
                fg=SOTET,
                bg=KARTYA,
            )
            ertek.pack(anchor="w", pady=(4, 0))
            self.kartyak[kulcs] = ertek

    def kartya(self, szulo, padx=17, pady=12):
        return tk.Frame(
            szulo,
            bg=KARTYA,
            padx=padx,
            pady=pady,
            highlightbackground="#e1e7f0",
            highlightthickness=1,
        )

    def bevitel_letrehoz(self, szulo):
        bal = self.kartya(szulo, padx=20)
        bal.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        tk.Label(
            bal,
            text="Új tanulási alkalom",
            bg=KARTYA,
            fg=SOTET,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        self.mezo(bal, "Dátum (ÉÉÉÉ-HH-NN)", self.datum)
        self.mezo(bal, "Tantárgy", self.tantargy, TANTARGYAK)
        self.mezo(bal, "Időtartam (perc)", self.perc)
        self.mezo(
            bal,
            "Koncentráció (1–5)",
            self.fokusz,
            ("1", "2", "3", "4", "5"),
            readonly=True,
        )
        self.mezo(bal, "Megjegyzés (nem kötelező)", self.megjegyzes)
        ttk.Button(
            bal,
            text="+ Alkalom hozzáadása",
            style="Main.TButton",
            command=self.hozzaad,
        ).pack(fill="x", pady=(4, 6))
        ttk.Button(
            bal,
            text="Mintaadatok betöltése",
            style="Alt.TButton",
            command=self.mintaadatok,
        ).pack(fill="x")
        tk.Label(
            bal,
            text="Az adatok automatikusan mentődnek a program mappájába.",
            bg=KARTYA,
            fg=MASODLAGOS,
            font=("Segoe UI", 9),
            wraplength=255,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

    def mezo(self, szulo, cim, valtozo, valaszthato=None, readonly=False):
        tk.Label(
            szulo,
            text=cim,
            bg=KARTYA,
            fg=MASODLAGOS,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 4))
        if valaszthato is None:
            mezo = ttk.Entry(szulo, textvariable=valtozo)
        else:
            mezo = ttk.Combobox(
                szulo,
                textvariable=valtozo,
                values=valaszthato,
                state="readonly" if readonly else "normal",
            )
        mezo.pack(fill="x", pady=(0, 6))

    def adatok_letrehoz(self, szulo):
        jobb = tk.Frame(szulo, bg=HATTER)
        jobb.grid(row=0, column=1, sticky="nsew")
        jobb.grid_rowconfigure(0, weight=3)
        jobb.grid_rowconfigure(1, weight=2)
        jobb.grid_columnconfigure(0, weight=1)

        self.tablazat_letrehoz(jobb)
        self.diagram_letrehoz(jobb)

    def tablazat_letrehoz(self, szulo):
        kartya = self.kartya(szulo, pady=14)
        kartya.grid(row=0, column=0, sticky="nsew", pady=(0, 13))
        kartya.grid_columnconfigure(0, weight=1)
        kartya.grid_rowconfigure(1, weight=1)

        fejlec = tk.Frame(kartya, bg=KARTYA)
        fejlec.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        tk.Label(
            fejlec,
            text="Bejegyzések",
            bg=KARTYA,
            fg=SOTET,
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left")
        self.szuro_mezo = ttk.Combobox(
            fejlec,
            textvariable=self.szuro,
            state="readonly",
            width=20,
        )
        self.szuro_mezo.pack(side="right")
        self.szuro_mezo.bind("<<ComboboxSelected>>", self.frissit)

        tabla_keret = tk.Frame(kartya, bg=KARTYA)
        tabla_keret.grid(row=1, column=0, sticky="nsew")
        oszlopok = ("datum", "tantargy", "perc", "fokusz", "megjegyzes")
        self.tabla = ttk.Treeview(
            tabla_keret,
            columns=oszlopok,
            show="headings",
            selectmode="browse",
            height=7,
        )
        fejlecek = (
            ("datum", "Dátum", 96),
            ("tantargy", "Tantárgy", 115),
            ("perc", "Perc", 60),
            ("fokusz", "Fókusz", 65),
            ("megjegyzes", "Megjegyzés", 170),
        )
        for azonosito, felirat, szelesseg in fejlecek:
            self.tabla.heading(azonosito, text=felirat)
            self.tabla.column(
                azonosito,
                width=szelesseg,
                minwidth=45,
                stretch=(azonosito == "megjegyzes"),
            )
        gorgeto = ttk.Scrollbar(
            tabla_keret, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=gorgeto.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        gorgeto.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self.kijeloles)

        lablec = tk.Frame(kartya, bg=KARTYA)
        lablec.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.darabszam = tk.Label(
            lablec,
            text="0 alkalom",
            bg=KARTYA,
            fg=MASODLAGOS,
            font=("Segoe UI", 9),
        )
        self.darabszam.pack(side="left")
        self.torles_gomb = ttk.Button(
            lablec,
            text="Kijelölt törlése",
            style="Danger.TButton",
            command=self.torol,
            state="disabled",
        )
        self.torles_gomb.pack(side="right")

    def diagram_letrehoz(self, szulo):
        kartya = self.kartya(szulo)
        kartya.grid(row=1, column=0, sticky="nsew")
        tk.Label(
            kartya,
            text="Tanulási idő tantárgyanként",
            bg=KARTYA,
            fg=SOTET,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")
        self.diagram = tk.Canvas(
            kartya, bg=KARTYA, highlightthickness=0, height=165
        )
        self.diagram.pack(fill="both", expand=True, pady=(8, 0))
        self.diagram.bind("<Configure>", self.diagram_rajzol)

    def bejegyzes_adatok(self):
        datum = self.datum.get().strip()
        tantargy = self.tantargy.get().strip()
        megjegyzes = self.megjegyzes.get().strip()

        try:
            if datetime.strptime(datum, "%Y-%m-%d").date().isoformat() != datum:
                raise ValueError
        except ValueError as hiba:
            raise ValueError("A dátum formátuma legyen ÉÉÉÉ-HH-NN.") from hiba

        try:
            perc = int(self.perc.get())
            fokusz = int(self.fokusz.get())
        except ValueError as hiba:
            raise ValueError(
                "A perc és a koncentráció egész szám legyen."
            ) from hiba

        if not 1 <= perc <= 720:
            raise ValueError("Az időtartam 1 és 720 perc közötti legyen.")
        if not 1 <= fokusz <= 5:
            raise ValueError("A koncentráció 1 és 5 közötti legyen.")
        if not 1 <= len(tantargy) <= 40:
            raise ValueError("A tantárgy neve 1–40 karakter lehet.")
        if len(megjegyzes) > 100:
            raise ValueError("A megjegyzés legfeljebb 100 karakter lehet.")

        return datum, tantargy, perc, fokusz, megjegyzes

    def hozzaad(self, esemeny=None):
        try:
            adatok = self.bejegyzes_adatok()
            self.naplo.hozzaad(*adatok)
        except ValueError as hiba:
            messagebox.showerror("Hibás adat", str(hiba))
            return
        except OSError as hiba:
            messagebox.showerror(
                "Mentési hiba", f"A bejegyzés mentése sikertelen: {hiba}"
            )
            return

        self.megjegyzes.set("")
        self.perc.set("45")
        self.szuro.set(SZURO_MIND)
        self.frissit()

    def kijeloles(self, esemeny=None):
        kijeloltek = self.tabla.selection()
        self.kijelolt_azonosito = kijeloltek[0] if kijeloltek else None
        self.torles_gomb.configure(
            state="normal" if kijeloltek else "disabled"
        )

    def torol(self):
        if not self.kijelolt_azonosito:
            return
        if not messagebox.askyesno(
            "Törlés megerősítése", "Biztosan törlöd a kijelölt alkalmat?"
        ):
            return
        try:
            self.naplo.torol(self.kijelolt_azonosito)
        except OSError as hiba:
            messagebox.showerror(
                "Mentési hiba", f"A módosítás mentése sikertelen: {hiba}"
            )
            return
        self.kijelolt_azonosito = None
        self.frissit()

    def mintaadatok(self):
        if self.naplo.bejegyzesek:
            messagebox.showwarning(
                "Nem üres napló",
                "A mintaadatok csak üres naplóba tölthetők be.",
            )
            return

        ma = date.today()
        mintak = (
            (6, "Programozás", 75, 5, "Python gyakorlás"),
            (5, "Matematika", 40, 3, "Feladatmegoldás"),
            (4, "Angol", 35, 4, "Olvasás"),
            (3, "Programozás", 60, 4, "Tkinter"),
            (2, "Fizika", 50, 3, "Jegyzetek"),
            (1, "Matematika", 90, 5, "Gyakorlófeladatok"),
        )
        alkalmak = [
            (
                (ma - timedelta(days=eltolodas)).isoformat(),
                tantargy,
                perc,
                fokusz,
                megjegyzes,
            )
            for eltolodas, tantargy, perc, fokusz, megjegyzes in mintak
        ]
        try:
            self.naplo.tobbet_hozzaad(alkalmak)
        except OSError as hiba:
            messagebox.showerror(
                "Mentési hiba", f"A mintaadatok mentése sikertelen: {hiba}"
            )
            return

        self.frissit()
        messagebox.showinfo(
            "Mintaadatok", "Hat tanulási alkalom sikeresen bekerült a naplóba."
        )

    def szurt_bejegyzesek(self):
        keresett = self.szuro.get()
        if keresett == SZURO_MIND:
            return list(self.naplo.bejegyzesek)
        return [
            sor
            for sor in self.naplo.bejegyzesek
            if sor["tantargy"] == keresett
        ]

    def frissit(self, esemeny=None):
        tantargyak = sorted(
            {sor["tantargy"] for sor in self.naplo.bejegyzesek},
            key=str.casefold,
        )
        valasztek = [SZURO_MIND, *tantargyak]
        self.szuro_mezo.configure(values=valasztek)
        if self.szuro.get() not in valasztek:
            self.szuro.set(SZURO_MIND)

        adatok = self.szurt_bejegyzesek()
        self.tablazat_frissit(adatok)
        self.statisztika_frissit(adatok)
        self.diagram_rajzol()

    def tablazat_frissit(self, adatok):
        for azonosito in self.tabla.get_children():
            self.tabla.delete(azonosito)
        rendezett = sorted(
            adatok,
            key=lambda sor: (sor["datum"], sor["id"]),
            reverse=True,
        )
        for sor in rendezett:
            self.tabla.insert(
                "",
                "end",
                iid=sor["id"],
                values=(
                    sor["datum"],
                    sor["tantargy"],
                    sor["perc"],
                    f'{sor["fokusz"]}/5',
                    sor["megjegyzes"],
                ),
            )
        self.kijeloles()
        self.darabszam.configure(text=f"{len(adatok)} alkalom")

    def statisztika_frissit(self, adatok):
        percek = [sor["perc"] for sor in adatok]
        osszes = sum(percek)
        self.kartyak["osszes"].configure(
            text=f"{osszes // 60} ó {osszes % 60} p"
        )
        mutatok = (
            ("atlag", atlag_perc),
            ("median", median_perc),
            ("szoras", szoras_perc),
        )
        for kulcs, szamitas in mutatok:
            ertek = f"{szamitas(percek):.1f} perc" if percek else "–"
            self.kartyak[kulcs].configure(text=ertek)

    def diagram_rajzol(self, esemeny=None):
        self.diagram.delete("all")
        adatok = aa_tantargyi_osszesites(self.szurt_bejegyzesek())
        szelesseg = max(self.diagram.winfo_width(), 400)
        magassag = max(self.diagram.winfo_height(), 90)
        if not adatok:
            self.diagram.create_text(
                szelesseg / 2,
                magassag / 2,
                text="Még nincs megjeleníthető adat.",
                fill=MASODLAGOS,
                font=("Segoe UI", 11),
            )
            return

        if len(adatok) > 5:
            maradek = sum(perc for _, perc in adatok[4:])
            adatok = [*adatok[:4], ("Továbbiak", maradek)]
        maximum = max(perc for _, perc in adatok)
        sav_magassag = max(17, min(36, (magassag - 24) // len(adatok)))
        sav_szelesseg = max(80, szelesseg - 220)
        szinek = (KEK, ZOLD, "#7d67d8", "#e6a145", "#5f8bac")

        for sorszam, (nev, ertek) in enumerate(adatok):
            y = 14 + sorszam * sav_magassag
            felirat = (nev[:16] + "…") if len(nev) > 16 else nev
            x0 = 135
            x1 = x0 + sav_szelesseg * ertek / maximum
            self.diagram.create_text(
                4,
                y,
                text=felirat,
                anchor="w",
                fill=SOTET,
                font=("Segoe UI", 10),
            )
            self.diagram.create_rectangle(
                x0,
                y - 8,
                x0 + sav_szelesseg,
                y + 8,
                fill="#eff3fa",
                outline="",
            )
            self.diagram.create_rectangle(
                x0,
                y - 8,
                x1,
                y + 8,
                fill=szinek[sorszam % len(szinek)],
                outline="",
            )
            self.diagram.create_text(
                x0 + sav_szelesseg + 9,
                y,
                text=f"{ertek} p",
                anchor="w",
                fill=MASODLAGOS,
                font=("Segoe UI", 10),
            )


def main():
    root = tk.Tk()
    try:
        app = AATanulasiAlkalmazas(root)
    except ValueError as hiba:
        messagebox.showerror(
            "Adatfájl hiba",
            f"{hiba}\n\nEllenőrizd a tanulasi_adatok.json fájlt.",
        )
        root.destroy()
        return
    root.mainloop()


if __name__ == "__main__":
    main()

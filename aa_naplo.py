import json
import uuid
from datetime import date
from pathlib import Path


class AANaplo:
    def __init__(self, fajl_utvonal):
        self.fajl_utvonal = Path(fajl_utvonal)
        self.bejegyzesek = []
        self.betolt()

    def betolt(self):
        if not self.fajl_utvonal.exists():
            self.bejegyzesek = []
            return
        try:
            with self.fajl_utvonal.open("r", encoding="utf-8") as fajl:
                adatok = json.load(fajl)
        except (OSError, ValueError) as hiba:
            raise ValueError("A mentett adatfájl nem olvasható.") from hiba
        if not isinstance(adatok, list):
            raise ValueError("A mentett adatok nem listában szerepelnek.")
        azonositok = set()
        for sor in adatok:
            if not self.ervenyes_bejegyzes(sor):
                raise ValueError("A mentett adatok között hibás bejegyzés van.")
            if sor["id"] in azonositok:
                raise ValueError("A mentett adatfájlban ismétlődő azonosító van.")
            azonositok.add(sor["id"])
        self.bejegyzesek = adatok

    def ervenyes_bejegyzes(self, sor):
        if not isinstance(sor, dict):
            return False
        kulcsok = ("id", "datum", "tantargy", "perc", "fokusz", "megjegyzes")
        if not all(kulcs in sor for kulcs in kulcsok):
            return False
        if not isinstance(sor["id"], str) or not sor["id"]:
            return False
        if not isinstance(sor["datum"], str):
            return False
        try:
            if date.fromisoformat(sor["datum"]).isoformat() != sor["datum"]:
                return False
        except ValueError:
            return False
        return (
            isinstance(sor["tantargy"], str)
            and 1 <= len(sor["tantargy"]) <= 40
            and type(sor["perc"]) is int
            and 1 <= sor["perc"] <= 720
            and type(sor["fokusz"]) is int
            and 1 <= sor["fokusz"] <= 5
            and isinstance(sor["megjegyzes"], str)
            and len(sor["megjegyzes"]) <= 100
        )

    def ment(self):
        self.fajl_utvonal.parent.mkdir(parents=True, exist_ok=True)
        ideiglenes = self.fajl_utvonal.with_suffix(".tmp")
        try:
            with ideiglenes.open("w", encoding="utf-8") as fajl:
                json.dump(self.bejegyzesek, fajl, indent=2, ensure_ascii=False)
            ideiglenes.replace(self.fajl_utvonal)
        finally:
            if ideiglenes.exists():
                ideiglenes.unlink()

    def uj_bejegyzes(self, datum, tantargy, perc, fokusz, megjegyzes):
        bejegyzes = {
            "id": uuid.uuid4().hex,
            "datum": datum,
            "tantargy": tantargy,
            "perc": perc,
            "fokusz": fokusz,
            "megjegyzes": megjegyzes,
        }
        if not self.ervenyes_bejegyzes(bejegyzes):
            raise ValueError("A tanulási alkalom egyik adata hibás.")
        return bejegyzes

    def hozzaad(self, datum, tantargy, perc, fokusz, megjegyzes):
        bejegyzes = self.uj_bejegyzes(
            datum, tantargy, perc, fokusz, megjegyzes
        )
        self.bejegyzesek.append(bejegyzes)
        try:
            self.ment()
        except OSError:
            self.bejegyzesek.pop()
            raise
        return bejegyzes

    def tobbet_hozzaad(self, alkalmak):
        ujak = [self.uj_bejegyzes(*alkalom) for alkalom in alkalmak]
        if not ujak:
            return 0
        self.bejegyzesek.extend(ujak)
        try:
            self.ment()
        except OSError:
            del self.bejegyzesek[-len(ujak):]
            raise
        return len(ujak)

    def torol(self, bejegyzes_azonosito):
        eredeti = self.bejegyzesek
        megtartott = [
            sor for sor in eredeti if sor["id"] != bejegyzes_azonosito
        ]
        if len(megtartott) == len(eredeti):
            return False
        self.bejegyzesek = megtartott
        try:
            self.ment()
        except OSError:
            self.bejegyzesek = eredeti
            raise
        return True


def aa_tantargyi_osszesites(bejegyzesek):
    percek_tantargyankent = {}
    for sor in bejegyzesek:
        tantargy = sor["tantargy"]
        percek_tantargyankent[tantargy] = (
            percek_tantargyankent.get(tantargy, 0) + int(sor["perc"])
        )
    return sorted(
        percek_tantargyankent.items(),
        key=lambda adat: (-adat[1], adat[0].casefold()),
    )

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from aa_naplo import AANaplo, aa_tantargyi_osszesites
from statisztika_bemutato import atlag_perc, median_perc, szoras_perc


class NaploTeszt(unittest.TestCase):
    def setUp(self):
        self.ideiglenes = tempfile.TemporaryDirectory()
        self.adatfajl = Path(self.ideiglenes.name) / "tesztadatok.json"
        self.naplo = AANaplo(self.adatfajl)

    def tearDown(self):
        self.ideiglenes.cleanup()

    def test_hozzaadas_es_betoltes(self):
        self.naplo.hozzaad("2026-11-12", "Programozás", 45, 5, "Gyakorlat")
        masolat = AANaplo(self.adatfajl)
        self.assertEqual(len(masolat.bejegyzesek), 1)
        self.assertEqual(masolat.bejegyzesek[0]["perc"], 45)
        self.assertEqual(masolat.bejegyzesek[0]["megjegyzes"], "Gyakorlat")

    def test_torles(self):
        sor = self.naplo.hozzaad("2026-11-12", "Matematika", 30, 4, "")
        self.assertTrue(self.naplo.torol(sor["id"]))
        self.assertFalse(self.naplo.torol(sor["id"]))
        self.assertEqual(AANaplo(self.adatfajl).bejegyzesek, [])

    def test_tantargyi_osszesites(self):
        adatok = [
            {"tantargy": "Angol", "perc": 30},
            {"tantargy": "Programozás", "perc": 45},
            {"tantargy": "Angol", "perc": 40},
        ]
        self.assertEqual(
            aa_tantargyi_osszesites(adatok),
            [("Angol", 70), ("Programozás", 45)],
        )

    def test_statisztika(self):
        adatok = [30, 45, 60]
        self.assertEqual(atlag_perc(adatok), 45)
        self.assertEqual(median_perc(adatok), 45)
        self.assertAlmostEqual(szoras_perc(adatok), 12.2474487139, places=6)
        self.assertEqual(atlag_perc([]), 0)
        self.assertEqual(median_perc([]), 0)
        self.assertEqual(szoras_perc([]), 0)

    def test_ervenytelen_adatfajl(self):
        self.adatfajl.write_text(json.dumps({"hibas": True}), encoding="utf-8")
        with self.assertRaises(ValueError):
            AANaplo(self.adatfajl)

    def test_serult_bejegyzes(self):
        self.adatfajl.write_text(
            json.dumps([{"id": "1", "datum": "nem dátum"}]),
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            AANaplo(self.adatfajl)

    def test_ervenytelen_bevitel(self):
        with self.assertRaises(ValueError):
            self.naplo.hozzaad("2026-11-12", "Programozás", -5, 5, "")
        self.assertFalse(self.adatfajl.exists())

    def test_mintaadatok_egy_mentessel(self):
        mintak = [
            ("2026-11-10", "Angol", 30, 4, "Olvasás"),
            ("2026-11-11", "Matematika", 40, 5, "Gyakorlás"),
        ]
        self.assertEqual(self.naplo.tobbet_hozzaad(mintak), 2)
        self.assertEqual(len(AANaplo(self.adatfajl).bejegyzesek), 2)
        self.assertEqual(self.naplo.tobbet_hozzaad([]), 0)

    def test_mentesi_hiba_eseten_hozzaadas_visszavonasa(self):
        with patch.object(self.naplo, "ment", side_effect=OSError("hiba")):
            with self.assertRaises(OSError):
                self.naplo.hozzaad("2026-11-12", "Angol", 30, 4, "")
        self.assertEqual(self.naplo.bejegyzesek, [])

    def test_mentesi_hiba_eseten_torles_visszavonasa(self):
        sor = self.naplo.hozzaad("2026-11-12", "Angol", 30, 4, "")
        with patch.object(self.naplo, "ment", side_effect=OSError("hiba")):
            with self.assertRaises(OSError):
                self.naplo.torol(sor["id"])
        self.assertEqual(len(self.naplo.bejegyzesek), 1)
        self.assertEqual(self.naplo.bejegyzesek[0]["id"], sor["id"])


if __name__ == "__main__":
    unittest.main()

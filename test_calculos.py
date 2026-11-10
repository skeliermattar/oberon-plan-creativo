"""Ejecutar: python3 -m unittest -v test_calculos.py"""
import unittest
from decimal import Decimal
from calculos import DatosInvalidos, calcular_plan, exportar_csv

PIEZAS = [{"tipo": "Pieza estática", "cantidad": 8, "horas": 1},
          {"tipo": "Carrusel", "cantidad": 3, "horas": 2},
          {"tipo": "Video corto", "cantidad": 2, "horas": 4}]


class PruebasPlan(unittest.TestCase):
    def plan(self, **cambios):
        datos = dict(campana="Campaña de prueba", piezas=PIEZAS, revisiones=20,
                     personas=1, horas_dia=4, plazo=5)
        datos.update(cambios)
        return calcular_plan(**datos)

    def test_ejemplo(self):
        r = self.plan()
        self.assertEqual(r["base"], 22)
        self.assertEqual(r["requeridas"], Decimal("26.4"))
        self.assertEqual(r["disponibles"], 20)
        self.assertEqual(r["diferencia"], Decimal("-6.4"))
        self.assertEqual(r["ocupacion"], 132)
        self.assertEqual(r["dias_necesarios"], 7)
        self.assertEqual(r["estado"], "Requiere ajuste")

    def test_capacidad_suficiente(self):
        r = self.plan(personas=2)
        self.assertEqual(r["estado"], "Capacidad suficiente")
        self.assertEqual(r["dias_necesarios"], 4)
        self.assertEqual(r["diferencia"], Decimal("13.6"))

    def test_capacidad_exacta_sin_margen(self):
        r = self.plan(piezas=[{"tipo": "Banner", "cantidad": 20, "horas": 1}], revisiones=0)
        self.assertEqual(r["estado"], "Capacidad justa")
        self.assertEqual(r["dias_necesarios"], 5)

    def test_entradas_invalidas(self):
        for cambio in [
            {"personas": 0}, {"horas_dia": 0}, {"plazo": 0}, {"revisiones": -1},
            {"horas_dia": "nan"}, {"horas_dia": "inf"}, {"personas": 1.5},
            {"plazo": 2.5}, {"campana": " "}, {"piezas": []},
            {"piezas": [{"tipo": "", "cantidad": 1, "horas": 1}]},
            {"piezas": [{"tipo": "Video", "cantidad": 1.2, "horas": 1}]},
            {"piezas": [{"tipo": "Video", "cantidad": 1, "horas": None}]},
        ]:
            with self.subTest(cambio=cambio), self.assertRaises(DatosInvalidos):
                self.plan(**cambio)

    def test_decimal_coma(self):
        r = self.plan(horas_dia="4,5")
        self.assertEqual(r["disponibles"], Decimal("22.5"))

    def test_redondeo_exacto(self):
        r = self.plan(piezas=[{"tipo": "Banner", "cantidad": 3, "horas": "0.3"}],
                      revisiones=0, horas_dia="0.3", plazo=3)
        self.assertEqual(r["dias_necesarios"], 3)

    def test_exportacion_y_texto_seguro(self):
        r = self.plan(campana="=1+1")
        texto = exportar_csv(r).decode("utf-8-sig")
        self.assertIn("'=1+1", texto)
        self.assertIn("26,40", texto)
        self.assertIn("Requiere ajuste", texto)


if __name__ == "__main__":
    unittest.main()

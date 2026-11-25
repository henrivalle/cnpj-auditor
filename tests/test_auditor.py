import csv
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from cnpj_auditor import classify


ROOT = Path(__file__).resolve().parents[1]
ALPHANUMERIC = "12ABC34501DE35"
NUMERIC = "00001234000153"


class ClassificationTests(unittest.TestCase):
    def test_official_example_and_numeric_example(self):
        self.assertEqual(classify(ALPHANUMERIC), "valido_alfanumerico")
        self.assertEqual(classify(" 12.abc.345/01de-35 "), "valido_alfanumerico")
        self.assertEqual(classify(NUMERIC), "valido_numerico")
        self.assertEqual(classify("00.001.234/0001-53"), "valido_numerico")

    def test_reports_common_spreadsheet_damage_without_repairing_it(self):
        cases = {
            "1234000153": "numerico_curto",
            "1.2E+13": "notacao_cientifica",
            "1,2e+13": "notacao_cientifica",
            "1E10": "notacao_cientifica",
            "12ABC34501DE36": "digitos_invalidos",
            "12ABC34501DEA5": "formato_invalido",
            "12 ABC34501DE35": "formato_invalido",
            "12.abc.345-01de/35": "formato_invalido",
            "１２ABC34501DE35": "formato_invalido",
            "12ÅBC34501DE35": "formato_invalido",
            "00000000000000": "formato_invalido",
            "": "vazio",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(classify(value), expected)

    def test_compact_cnpj_shape_has_priority_over_exponent_heuristic(self):
        self.assertEqual(classify("0123456789E046"), "valido_alfanumerico")


class CliTests(unittest.TestCase):
    def run_audit(self, data, *args):
        with tempfile.TemporaryDirectory() as folder:
            fixture = Path(folder) / "input.csv"
            fixture.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)
            return subprocess.run(
                [sys.executable, "-m", "cnpj_auditor", str(fixture), *args],
                cwd=ROOT, capture_output=True, text=True,
            )

    def test_audits_utf8_bom_and_reports_physical_lines_without_values(self):
        result = self.run_audit(
            f'\ufeffregistro;empresa\n{ALPHANUMERIC};"teste\nde planilha"\n'
            '1,2E+13;texto-privado\n\nshort;campo;extra\n"";vazio\n',
            "--coluna", "registro", "--delimitador", "ponto-e-virgula",
        )
        rows = list(csv.reader(io.StringIO(result.stdout)))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(rows, [
            ["linha", "status"],
            ["2", "valido_alfanumerico"],
            ["4", "notacao_cientifica"],
            ["6", "colunas_inconsistentes"],
            ["7", "vazio"],
        ])
        for private_value in (ALPHANUMERIC, "texto-privado", "1,2E+13"):
            self.assertNotIn(private_value, result.stdout + result.stderr)

    def test_numeric_data_passes_but_ci_can_require_an_alphanumeric_example(self):
        source = f"cnpj\n{NUMERIC}\n"
        self.assertEqual(self.run_audit(source).returncode, 0)
        result = self.run_audit(source, "--exigir-alfanumerico")
        self.assertEqual(result.returncode, 1)
        self.assertIn("alfanumérico válido", result.stderr)
        result = self.run_audit(source + f"{ALPHANUMERIC}\n", "--exigir-alfanumerico")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_tab_delimiter(self):
        result = self.run_audit(f"lote\tcnpj\na\t{NUMERIC}\n", "--delimitador", "tab")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2,valido_numerico", result.stdout)

    def test_unusable_input_exits_two(self):
        for data in (
            "",
            "cnpj\n",
            f"outra\n{NUMERIC}\n",
            f"cnpj,cnpj\n{NUMERIC},{NUMERIC}\n",
            'cnpj\n"valor-privado\n',
            b"cnpj\n\xff",
        ):
            with self.subTest(data=data):
                result = self.run_audit(data)
                self.assertEqual(result.returncode, 2)
                self.assertTrue(result.stderr)
                self.assertNotIn("valor-privado", result.stderr)


if __name__ == "__main__":
    unittest.main()

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class ExportacaoCliTest(unittest.TestCase):
    def test_exemplo_completo(self):
        comando = [sys.executable, "-X", "utf8", str(ROOT / "app.py"), str(ROOT / "exemplo.json")]
        dados = subprocess.check_output([*comando, '--markdown']).decode("utf-8")
        padrao = json.loads(subprocess.check_output(comando))
        self.assertEqual(dados, padrao['markdown'] + "\n")

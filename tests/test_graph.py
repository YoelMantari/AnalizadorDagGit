import unittest
import os
import sys
from unittest.mock import patch

# agrega directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from graph_analysis import analizador_dag

class test_dag(unittest.TestCase):
    def setUp(self):
        # crea analizador para cada test
        self.analizador = analizador_dag()
        
    def test_densidad_basica(self):
        # test simple de densidad
        self.analizador.commits = {"a": True, "b": True}
        self.analizador.padres = {"a": [], "b": ["a"]}
        
        densidad = self.analizador.calcular_densidad_ramas()
        self.assertGreater(densidad, 0)
        
    def test_entropia_simple(self):
        # test simple de entropia
        self.analizador.commits = {"a": True, "b": True}
        self.analizador.padres = {"a": [], "b": ["a"]}
        
        entropia = self.analizador.calcular_entropia()
        self.assertGreaterEqual(entropia, 0)
        
    @patch('subprocess.check_output')
    def test_mock_git(self, mock_subprocess):
        # test con mock de git
        mock_subprocess.return_value = "abc123 def456\ndef456\n"
        
        resultado = self.analizador.obtener_commits_git("/fake/repo")
        self.assertTrue(resultado)

if __name__ == "__main__":
    unittest.main()

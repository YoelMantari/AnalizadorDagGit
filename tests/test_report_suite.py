import unittest
import tempfile
import json
import os
import sys
from unittest.mock import Mock

# se agrega src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from report_suite import commit_stats_service, release_notes_service, changelog_writer, reporting_suite, read_json_file

class test_report_suite(unittest.TestCase):
    
    def test_stats_service(self):
        # test de las metricas
        mock_reader = Mock(return_value={"densidad_ramas": 1.5, "entropia_historia": 0.8})
        service = commit_stats_service(mock_reader)
        
        stats = service.get_stats("fake.json")
        self.assertEqual(stats["densidad"], 1.5)
        
    def test_facade_completo(self):
        # test de facade, crea json temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"densidad_ramas": 2.0, "entropia_historia": 1.0}, f)
            json_path = f.name
        
        try:
            # se crea servicios
            stats_service = commit_stats_service(read_json_file)
            notes_service = release_notes_service()
            writer = changelog_writer(notes_service)
            
            # se crea facade
            suite = reporting_suite(stats_service, notes_service, writer)
            
            # generamos reporte
            output_file = suite.generate_report(json_path)
            
            # se verifica que se creo
            self.assertTrue(os.path.exists(output_file))
            
            os.unlink(output_file)
            
        finally:
            os.unlink(json_path)

if __name__ == "__main__":
    unittest.main()
import unittest
from visualizer import DependencyVisualizer
import json
from unittest.mock import patch, mock_open

class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.config = {
            "plantuml_path": "path/to/plantuml.jar",
            "output_path": "graph.png",
            "url": "http://example.com/dependencies.json",
        }

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "dependencies": [
            {"name": "A", "dependencies": ["B", "C"]},
            {"name": "B", "dependencies": ["D"]},
            {"name": "C", "dependencies": []},
            {"name": "D", "dependencies": []}
        ]
    }))
    def test_parse_dependencies(self, mock_file):
        visualizer = DependencyVisualizer("config.json")
        graph = visualizer.parse_dependencies("dependencies.json")
        expected_graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": [],
            "D": []
        }
        self.assertEqual(graph, expected_graph)

    @patch("urllib.request.urlopen")
    def test_download_dependencies_file(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = b'{}'
        visualizer = DependencyVisualizer("config.json")
        file_path = visualizer.download_dependencies_file()
        self.assertTrue(file_path.exists())

if __name__ == "__main__":
    unittest.main()

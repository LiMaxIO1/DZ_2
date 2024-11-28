import os
import json
import subprocess
import urllib.request
from pathlib import Path


class DependencyVisualizer:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)

    def _load_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def download_dependencies_file(self):
        url = self.config['url']
        local_file = Path("dependencies.json")  # Временный файл
        print(f"Downloading dependencies from {url}")
        with urllib.request.urlopen(url) as response:
            with open(local_file, 'wb') as f:
                f.write(response.read())
        return local_file

    def parse_dependencies(self, dependencies_file):
        with open(dependencies_file, 'r') as f:
            data = json.load(f)

        graph = {}
        for package in data.get("dependencies", []):
            name = package["name"]
            deps = package.get("dependencies", [])
            graph[name] = deps
        return graph

    def generate_plantuml(self, graph):
        lines = ["@startuml"]
        for node, dependencies in graph.items():
            for dep in dependencies:
                lines.append(f'"{node}" --> "{dep}"')
        lines.append("@enduml")

        output_file = Path("dependencies.puml")
        with open(output_file, 'w') as f:
            f.write("\n".join(lines))
        return output_file

    def render_graph(self, plantuml_file):
        output_path = self.config['output_path']
        plantuml_path = self.config['plantuml_path']

        # Проверяем, что файл действительно существует
        if not os.path.exists(plantuml_file):
            print(f"Error: PlantUML file {plantuml_file} does not exist.")
            return

        try:
            subprocess.run(["java", "-jar", plantuml_path, plantuml_file], check=True)
            print(f"Graph saved to {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during PlantUML execution: {e}")

    def run(self):
        dependencies_file = self.download_dependencies_file()
        graph = self.parse_dependencies(dependencies_file)

        # Сначала генерируем .puml файл
        plantuml_file = self.generate_plantuml(graph)

        # Теперь рендерим граф, используя существующий .puml файл
        self.render_graph(plantuml_file)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python visualizer.py <config_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    visualizer = DependencyVisualizer(config_path)
    visualizer.run()

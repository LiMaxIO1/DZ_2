import subprocess

def visualize_graph(plantuml_path, puml_file):
    result = subprocess.run(
        ["java", "-jar", plantuml_path, puml_file],
        capture_output=True
    )
    if result.returncode != 0:
        raise Exception("Ошибка визуализации графа")

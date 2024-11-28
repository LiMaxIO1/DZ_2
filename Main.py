import json
import sys
from dependency_parser import parse_dependencies
from graph_generator import generate_plantuml
from visualizer import visualize_graph

def main(config_path):
    try:
        # Чтение конфигурации
        with open(config_path, 'r') as file:
            config = json.load(file)

        # Извлечение зависимостей
        dependencies = parse_dependencies(config["repository_url"], config["package_name"])

        # Генерация графа PlantUML
        plantuml_path = generate_plantuml(dependencies, config["output_path"])

        # Визуализация графа
        visualize_graph(config["visualizer_path"], plantuml_path)

        print("Граф зависимостей успешно создан!")
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config.json>")
        sys.exit(1)
    main(sys.argv[1])

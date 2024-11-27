import json
import os
import subprocess
import requests

# Чтение конфигурации
with open('config.json') as f:
    config = json.load(f)

visualization_program_path = config['visualization_program_path']
package_name = config['package_name']
output_image_path = config['output_image_path']
repository_url = config['repository_url']

# Функция для получения зависимостей пакета
def get_dependencies(package_name, repository_url):
    # В реальной задаче нужно парсить POM или использовать Maven API
    # Для простоты, предположим, что зависимости можно получить по URL
    url = f"{repository_url}/{package_name.replace(':', '/')}/maven-metadata.xml"
    response = requests.get(url)
    if response.status_code == 200:
        # Разобрать XML и получить зависимости
        return []  # Вернуть список зависимостей
    return []

# Генерация файла PlantUML
def generate_plantuml_file(dependencies, output_file):
    with open(output_file, 'w') as f:
        f.write("@startuml\n")
        f.write(f"package \"{package_name}\" {{\n")
        for dep in dependencies:
            f.write(f"  [{dep}]\n")
        f.write("}\n")
        f.write("@enduml\n")

# Получение зависимостей
dependencies = get_dependencies(package_name, repository_url)

# Генерация файла PlantUML
puml_file = 'dependencies_graph.puml'
generate_plantuml_file(dependencies, puml_file)

# Визуализация с помощью PlantUML
subprocess.run([visualization_program_path, puml_file])

# Перемещение файла в нужную директорию
os.rename('dependencies_graph.png', output_image_path)

print(f"Граф зависимостей успешно сохранен в {output_image_path}")

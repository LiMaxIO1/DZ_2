import json
import subprocess
import os

def load_config(config_path):
    """Загрузка конфигурации из файла"""
    with open(config_path, 'r') as f:
        return json.load(f)

def generate_puml_from_dependencies(dependencies, output_path):
    """Генерация файла PlantUML для визуализации зависимостей"""
    puml_content = "@startuml\n"
    puml_content += "skinparam rectangle { BackgroundColor LightYellow }\n"

    for dep in dependencies:
        # Формируем строку для каждой зависимости
        puml_content += f'"{dep}"\n'

    puml_content += "@enduml"
    
    with open(output_path, 'w') as puml_file:
        puml_file.write(puml_content)

def generate_image_from_puml(puml_file, image_file, plantuml_path):
    """Использование PlantUML для генерации изображения из PUML файла"""
    # Проверяем, что PlantUML доступен
    if not os.path.exists(plantuml_path):
        print(f"Ошибка: не найден файл PlantUML по пути {plantuml_path}")
        return

    # Запуск PlantUML для генерации изображения
    subprocess.run([plantuml_path, puml_file])

    # Переименование выходного файла в нужное имя
    os.rename(f'{puml_file.replace(".puml", ".png")}', image_file)
    print(f"Граф зависимостей успешно сохранен в {image_file}")

def main():
    # Путь к конфигурационному файлу
    config_path = '/config.json'
    config = load_config(config_path)

    # Извлекаем настройки из конфигурации
    package_name = config["package_name"]
    output_image_path = config["output_image_path"]
    plantuml_path = config["visualization_program_path"]

    # Здесь мы используем фиктивные зависимости для примера
    # В реальной ситуации зависимости можно анализировать на основе файла pom.xml
    dependencies = [
        "com.google.guava:guava:30.1-jre",
        "org.apache.commons:commons-lang3:3.12.0",
        "org.springframework:spring-core:5.3.8"
    ]
    
    # Генерация PUML файла
    puml_file = 'dependencies_graph.puml'
    generate_puml_from_dependencies(dependencies, puml_file)
    
    # Генерация PNG изображения из PUML файла
    generate_image_from_puml(puml_file, output_image_path, plantuml_path)

if __name__ == '__main__':
    main()

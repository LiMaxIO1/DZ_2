def generate_plantuml(dependencies, output_path):
    puml_path = output_path.replace(".png", ".puml")

    with open(puml_path, 'w') as file:
        file.write("@startuml\n")
        file.write("digraph dependencies {\n")

        for dep, version in dependencies.items():
            file.write(f'"{dep}" [label="{dep}\\n{version}"];\n')

        file.write("}\n")
        file.write("@enduml\n")

    return puml_path

import requests
from xml.etree import ElementTree

def parse_dependencies(repository_url, package_name):
    response = requests.get(f"{repository_url}/{package_name}/pom.xml")
    if response.status_code != 200:
        raise Exception("Не удалось загрузить pom.xml")

    root = ElementTree.fromstring(response.content)
    dependencies = {}
    
    for dependency in root.findall(".//dependency"):
        group_id = dependency.find("groupId").text
        artifact_id = dependency.find("artifactId").text
        version = dependency.find("version").text
        dependencies[f"{group_id}:{artifact_id}"] = version

    return dependencies

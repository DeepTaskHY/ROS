import json
import os
import re
import rospkg
import time
from xml.etree.ElementTree import Element, parse


def get_package_path(package_name: str) -> str:
    return rospkg.RosPack().get_path(package_name)


def get_configuration_path(package_name: str) -> str:
    return os.path.join(get_package_path(package_name), 'configuration.json')


def get_authorization_path(package_name: str) -> str:
    return os.path.join(get_package_path(package_name), 'keys')


def get_key_path(package_name: str, key_file: str) -> str:
    return os.path.join(get_authorization_path(package_name), key_file)


def get_scenario_path(package_name: str) -> str:
    return os.path.join(get_package_path(package_name), 'scenarios')


def get_configuration(package_name: str) -> dict:
    with open(get_configuration_path(package_name)) as json_file:
        configuration = json.load(json_file)

    return configuration


def get_module_configuration(package_name: str, module_name: str) -> dict:
    return get_configuration(package_name)['modules'][module_name]


def get_test_configuration(package_name: str, test_name: str) -> dict:
    return get_configuration(package_name)['tests'][test_name]


# Timestamp string
def timestamp() -> str:
    return str(time.time())


# Check message language
def is_hangul(text: str) -> bool:
    hangul_count = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
    return hangul_count > 0


# Reverse AM:PM
def reverse_time(time: str) -> str:
    if not time:
        return None

    hour = int(time[0:2])
    min = int(time[3:5])

    # to PM
    if hour < 12:
        return f'{hour + 12}:{min}'

    # to AM (zero padding)
    elif hour - 12 < 10:
        return f'0{hour - 12}:{min}'

    # to AM
    return f'{hour - 12}:{min}'


class XMLParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tree = parse(file_path)

    @property
    def root(self) -> Element:
        return self.tree.getroot()

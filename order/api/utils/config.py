import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
config = configparser.ConfigParser()
config.read(f"{BASE_DIR}/config.ini")

conf_api_endpoints = config["api-endpoints"]

def get_api_endpoints() -> dict:
    endpoints: dict = {}

    for section in conf_api_endpoints:
        endpoints[section.upper()] = conf_api_endpoints[section.upper()]
    
    return endpoints

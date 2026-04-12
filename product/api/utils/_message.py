import configparser

config = configparser.ConfigParser()
config.read("config.ini")

conf_messages = config["messages"]
conf_api_massages = config["api-response-messages"]

global_message_keys = None
api_message_keys = None

def get_global_messages() -> dict:
    messages: dict = {}

    for section in conf_messages:
        messages[section.upper()] = conf_messages[section.upper()]
    
    return messages

def get_api_response_messages() -> dict:
    messages: dict = {}

    for section in conf_api_massages:
        messages[section.upper()] = conf_api_massages[section.upper()]
    
    return messages

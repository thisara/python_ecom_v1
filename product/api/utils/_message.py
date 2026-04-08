import configparser

config = configparser.ConfigParser()
config.read("config.ini")

conf_messages = config["messages"]
conf_api_massages = config["api-response-messages"]

def get_global_messages() -> dict:
    print("Messages initiated!")
    messages: dict = {}

    for section in conf_messages:
        messages[section.upper()] = conf_messages[section.upper()]
    
    """
    messages: dict = {
        'SUCCESS_SAVE':conf_messages['SUCCESS_SAVE'],
        'ERROR_SAVE':conf_messages['ERROR_SAVE'],
        'SUCCESS_UPDATE':conf_messages['SUCCESS_UPDATE'],
        'ERROR_UPDATE':conf_messages['ERROR_UPDATE'],
        'SERVER_ERROR':conf_messages['SERVER_ERROR']
    }
    """
    return messages

def get_api_response_messages() -> dict:
    print("API Messages initiated!")
    messages: dict = {}

    for section in conf_api_massages:
        messages[section.upper()] = conf_api_massages[section.upper()]
    
    """
    messages: dict = {
        'PRODUCT_NOT_FOUND': conf_api_massages['PRODUCT_NOT_FOUND'],
        'INVALID_STOCK_DATA': conf_api_massages['INVALID_STOCK_DATA'],
        'PRODUCT_EXIST': conf_api_massages['PRODUCT_EXIST'],
        'PRODUCT_CREATED': conf_api_massages['PRODUCT_CREATED'],
        'INVALID_PRODUCT_DATA': conf_api_massages['INVALID_PRODUCT_DATA']
    }
    """
    return messages


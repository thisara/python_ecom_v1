
OK="OK"
ERR="ERR"
DUP="DUP"
LOW="LOW"
VER="VER"
NO_PROD="NO_PROD"
NO_PROD_DATA="NO_PROD_DATA"

def resp_codes() -> dict:

    codes: dict = {
        "OK" : "SUCCESS",
        "ERR" : "FAILURE",
        "DUP" : "EXIST",
        "LOW" : "LOW STOCK",
        "VER" : "VERSION MISMATCH",
        "NO_PROD" : "NO PRODUCT",
        "NO_PROD_DATA" : "NO PRODUCT DATA"
    }

    return codes

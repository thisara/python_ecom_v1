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

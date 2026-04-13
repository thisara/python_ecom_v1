def resp_codes() -> dict:

    codes: dict = {
        "OK" : "SUCCESS",
        "ERR" : "FAILURE",
        "DUP" : "EXIST",
        "LOW" : "LOW STOCK",
        "VER" : "VERSION MISMATCH"
    }

    return codes


ERR: str = 'ERR'
DUP: str = 'DUP'
OK: str = 'OK'
NON: str = 'NON'
PAR: str = 'PAR'

def resp_codes() -> dict:

    codes: dict = {
        OK : "SUCCESS",
        ERR : "FAILURE",
        DUP : "EXIST",
        NON : "NO_ITEMS_MATCHED",
        PAR : "PARTIAL_ITEMS_MATCHED"
    }

    return codes


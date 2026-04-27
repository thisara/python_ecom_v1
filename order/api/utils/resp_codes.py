
ERR: str = 'ERR'
DUP: str = 'DUP'
OK: str = 'OK'

def resp_codes() -> dict:

    codes: dict = {
        OK : "SUCCESS",
        ERR : "FAILURE",
        DUP : "EXIST"
    }

    return codes


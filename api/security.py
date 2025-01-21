import schemas.security
import util.string

from fastapi import APIRouter, HTTPException

security_router = APIRouter()


@security_router.post("/encrypt", status_code=200)
def encrypt(string: schemas.security.SecurityCreate):
    try:
        encrypted_string = util.string.encrypt_str(string.string)

        return {"encrypted_string": encrypted_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@security_router.post("/decrypt", status_code=200)
def decrypt(string: schemas.security.SecurityCreate):
    try:
        decrypted_string = util.string.decrypt_str(string.string)

        return {"decrypted_string": decrypted_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
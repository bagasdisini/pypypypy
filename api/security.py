from fastapi import APIRouter, status, HTTPException

import schemas.security
import util.string

security_router = APIRouter()


@security_router.post("/encrypt", status_code=status.HTTP_200_OK)
def encrypt(string: schemas.security.SecurityCreate):
    try:
        encrypted_string = util.string.encrypt_str(string.string)
        return {"encrypted_string": encrypted_string}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@security_router.post("/decrypt", status_code=status.HTTP_200_OK)
def decrypt(string: schemas.security.SecurityCreate):
    try:
        decrypted_string = util.string.decrypt_str(string.string)
        return {"decrypted_string": decrypted_string}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
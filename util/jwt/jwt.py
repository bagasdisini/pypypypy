from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import BaseModel

import core.config


security = HTTPBearer()


class UserClaims(BaseModel):
    id: str
    email: str
    role: str
    session_id: str
    expired_date_in_millis: int

    @property
    def is_expired(self) -> bool:
        return self.expired_date_in_millis < int(datetime.now(tz=timezone.utc).timestamp() * 1000)


def decode_jwt(token: str) -> UserClaims:
    try:
        payload = jwt.decode(token, core.config.Config.AUTH_JWT_KEY, algorithms=[core.config.CONST_JWT_ALGORITHM])
        claims = UserClaims(**payload)
        if claims.is_expired:
            raise HTTPException(status_code=401, detail="Token has expired")
        return claims
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserClaims:
    token = credentials.credentials
    return decode_jwt(token)


def create_jwt_token(user_id: str, email: str, role: str, session_id: str) -> str:
    expiration = datetime.now(tz=timezone.utc) + timedelta(days=core.config.Config.AUTH_JWT_EXPIRE)
    payload = {
        "id": user_id,
        "email": email,
        "role": role,
        "session_id": session_id,
        "expired_date_in_millis": int(expiration.timestamp() * 1000),
        "exp": expiration
    }
    token = jwt.encode(payload, core.config.Config.AUTH_JWT_KEY, algorithm=core.config.CONST_JWT_ALGORITHM)
    return token

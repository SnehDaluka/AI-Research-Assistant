from functools import lru_cache

from backend.bootstrap import startup


@lru_cache
def get_application():

    return startup()

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_jwt_key_for_ai_research_assistant")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
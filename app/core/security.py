from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer()
ALGO = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

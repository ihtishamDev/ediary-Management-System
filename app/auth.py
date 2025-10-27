from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os
from fastapi import HTTPException, Request
from .db import SessionLocal
from .models import User

SECRET = os.getenv('JWT_SECRET', 'dev-secret-change-me')
ALGO = 'HS256'
ACCESS_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def _truncate_to_72_bytes(s: str) -> str:
    b = s.encode('utf-8')
    if len(b) > 72:
        b = b[:72]                    # truncate bytes
        return b.decode('utf-8', 'ignore')  # drop any broken tail
    return s

def hash_password(password: str) -> str:
    pwd = _truncate_to_72_bytes(password)
    return pwd_context.hash(pwd)

def verify_password(plain: str, hashed: str) -> bool:
    plain_trunc = _truncate_to_72_bytes(plain)
    return pwd_context.verify(plain_trunc, hashed)


def create_access_token(subject: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET, algorithm=ALGO)

def decode_token(token: str) -> dict:
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')

from fastapi import Depends

def get_current_user(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')
    payload = decode_token(token)
    sub = payload.get('sub')
    if not sub:
        raise HTTPException(status_code=401, detail='Invalid token payload')
    db = SessionLocal()
    user = db.query(User).filter(User.email == sub).first()
    db.close()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user

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

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

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
    
# dependency to get current user from cookie
from fastapi import Depends

def get_current_user(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')
    payload = decode_token(token)
    sub = payload.get('sub')
    # print(sub)
    if not sub:
        raise HTTPException(status_code=401, detail='Invalid token payload')
    db = SessionLocal()
    user = db.query(User).filter(User.email == sub).first()
    db.close()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user

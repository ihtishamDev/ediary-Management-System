from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..schemas import UserCreate, UserOut
from ..db import SessionLocal
from ..models import User
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter()
@router.post('/register', response_model=UserOut)
def register(payload: UserCreate):
    db = SessionLocal()
    if db.query(User).filter(User.email == payload.email).first():
        db.close()
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(name=payload.name, email=payload.email,
password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    out = UserOut.from_orm(user)
    db.close()
    return out

@router.post('/login')
def login(payload: UserCreate):
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        db.close()
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token(user.email)
    res = JSONResponse({"msg": "ok"})
    # In dev set secure=False; in production, secure=True
    res.set_cookie('access_token', token, httponly=True, samesite='lax')
    db.close()
    return res

@router.post('/logout')
def logout():
    res = JSONResponse({"msg": "logged out"})
    res.delete_cookie('access_token')
    return res

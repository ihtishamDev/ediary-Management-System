import secrets
from ..models import User
from ..db import SessionLocal
from ..utils import send_email
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse , HTMLResponse
from fastapi import APIRouter, HTTPException, BackgroundTasks
from ..auth import hash_password, verify_password, create_access_token
from ..schemas import (
    UserCreate,
    UserOut,
    UserCreatelogin,
    ForgetPassword,
    ResetPassword,
    VerifyEmailRequest,
)

router = APIRouter()


# ---------- Register ----------
@router.post('/register', response_model=UserOut)
def register(payload: UserCreate, background: BackgroundTasks):
    db = SessionLocal()
    if db.query(User).filter(User.email == payload.email).first():
        db.close()
        raise HTTPException(status_code=400, detail='Email already registered')

    token = secrets.token_urlsafe(32)
    


    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_verified=False,
        verification_token=token,
        verification_token_expires=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # build verification link
    verify_link = f"http://localhost:8000/auth/verify?token={token}"

    # send verification mail
    background.add_task(
        send_email,
        to=user.email,
        subject="Verify your email",
        body=f"Hi {user.name},\n\nPlease click the link to verify your account:\n{verify_link}\n\nThis link expires in 1 hour."
    )

    db.close()
    return UserOut.from_orm(user)


# ---------- Verify Email ----------
@router.get("/verify")
def verify_email(token: str , response_class=HTMLResponse):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.verification_token == token).first()

        if not user or not user.verification_token_expires or user.verification_token_expires < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        db.commit()

         # 🎨 Styled HTML message
        html_content = """
        <html>
            <head>
                <title>Email Verification</title>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background: #f4f7fa;
                        font-family: Arial, sans-serif;
                    }
                    .message-box {
                        text-align: center;
                        background: white;
                        padding: 30px 40px;
                        border-radius: 12px;
                        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
                    }
                    .message-box h2 {
                        color: #2c3e50;
                        margin-bottom: 15px;
                    }
                    .message-box p {
                        font-size: 16px;
                        color: #555;
                    }
                </style>
            </head>
            <body>
                <div class="message-box">
                    <h2>✅ Email Verified Successfully!</h2>
                    <p>You can now login to your account.</p>
                </div>
            </body>
        </html>
        """
        
        return HTMLResponse(content=html_content, status_code=200)

    finally:
        db.close()


# ---------- Login ----------

@router.post('/login')
def login(payload: UserCreatelogin):
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        db.close()
        raise HTTPException(status_code=401, detail='Invalid credentials')

    if not user.is_verified:
        db.close()
        raise HTTPException(status_code=403, detail="Please verify your email before login")

    token = create_access_token(user.email)
    res = JSONResponse({"msg": "ok"})
    res.set_cookie('access_token', token, httponly=True, samesite='lax')
    print("access_token is here", token)
    db.close()
    return res


# ---------- Logout ----------
@router.post('/logout')
def logout():
    res = JSONResponse({"msg": "logged out"})
    res.delete_cookie('access_token')
    return res


# ---------- Forgot password ----------
@router.post("/forgetpassword")
def forget_password(payload: ForgetPassword, background: BackgroundTasks):
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    # generate token + expiry
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    reset_link = f"http://localhost:3000/reset-password?token={token}"

    background.add_task(
        send_email,
        to=user.email,
        subject="Password Reset",
        body=f"Click here to reset your password:\n{reset_link}"
    )
    db.close()
    return {"message": "Reset link sent to your email"}


# ---------- Reset password ----------
@router.post("/resetpassword")
def reset_password(payload: ResetPassword):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.reset_token == payload.token).first()

        if not user or user.reset_token_expires is None or user.reset_token_expires < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        if payload.new_password != payload.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        user.password_hash = hash_password(payload.new_password)
        user.reset_token = None
        user.reset_token_expires = None

        db.commit()
        return {"message": "Password updated successfully"}
    finally:
        db.close()

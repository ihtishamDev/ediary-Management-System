import secrets
from ..models import User
from ..db import SessionLocal
from app.utils import send_email  # your Resend function
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse , HTMLResponse , RedirectResponse
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from ..auth import hash_password, verify_password, create_access_token , get_current_user
from ..schemas import (
    UserCreate,
    UserOut,
    UserCreatelogin,
    ForgetPassword,
    ResetPassword,
    VerifyEmailRequest,
    UserUpdate,
    updatePassword,
)

router = APIRouter()


# ---------- Register ----------
# @router.post('/register', response_model=UserOut)
# def register(payload: UserCreate, background: BackgroundTasks):
#     db = SessionLocal()
#     if db.query(User).filter(User.email == payload.email).first():
#         db.close()
#         raise HTTPException(status_code=400, detail='Email already registered')

#     token = secrets.token_urlsafe(32)
  
#     user = User(
#         name=payload.name,
#         email=payload.email,
#         password_hash=hash_password(payload.password),
#         phone_number = payload.phone_number ,
#         gender = payload.gender,
#         address = payload.address,
#         is_verified=False,
#         verification_token=token,
#         verification_token_expires=datetime.utcnow() + timedelta(hours=1)
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     # build verification link
#     # BASE_URL = "https://ediary-management-system-production.up.railway.app"

#     verify_link = f"http://localhost:8000/auth/verify?token={token}"

#     # send verification mail
#     background.add_task(
#         send_email,
#         to=user.email,
#         subject="Verify your email",
#         body=f"Hi {user.name},\n\nPlease click the link to verify your account:\n{verify_link}\n\nThis link expires in 1 hour."
#     )
#     db.close()
#     return UserOut.from_orm(user)





@router.post("/register")
def register_user(payload: UserCreate):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        token = secrets.token_urlsafe(32)
        # expiry = datetime.utcnow() + timedelta(hours=1)

        new_user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        phone_number = payload.phone_number ,
        gender = payload.gender,
        address = payload.address,
        is_verified=False,
        verification_token=token,
        verification_token_expires=datetime.utcnow() + timedelta(hours=1)
        )
        db.add(new_user)
        db.commit()

        # verify_link = f"https://ediary-management-system-production.up.railway.app/verify?token={token}"
        verify_link = f"http://localhost:8000/auth/verify?token={token}"

        

        subject = "Verify Your Email - Shami App"
        body = f"""
        <h2>Welcome!</h2>
        <p>Click the link below to verify your email:</p>
        <a href="{verify_link}" target="_blank">Verify Email</a>
        <br><br>
        <small>This link will expire in 1 hour.</small>
        """

        send_email(to=payload.email, subject=subject, body=body)

        return {"msg": "User registered successfully. Verification email sent!"}

    except Exception as e:
        print("❌ Error in register:", e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()



@router.put("/changepassword" )
def change_password(payload: updatePassword , current_user: User = Depends(get_current_user) ):
    db = SessionLocal()
    try: 
        user = db.query(User).filter(User.id == current_user.id).first()
    
        if not user:
            raise HTTPException(status_code=404 , detail="User not found")
    
        if not verify_password(payload.old_password , user.password_hash):
            raise HTTPException(
                status_code=404, detail="Old Password does not match"
        )
    
        new_hashed_password  = hash_password(payload.new_password)
        user.password_hash = new_hashed_password 
        db.commit()

        print("udpatepasswordudpatepassword" , {new_hashed_password })
        print("udpatepasswordudpatepassword" , new_hashed_password )
    
        return new_hashed_password 
    finally:
        db.close()

# ---------- Verify Email ----------
@router.get("/verify")
def verify_email(token: str , response_class=HTMLResponse):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.verification_token == token).first()



        if not user:
            db.close()
            return RedirectResponse (url="http://localhost:3000?msg=invalid_token")
        
        if user.verification_token_expires < datetime.utcnow():
            return RedirectResponse (url="http://localhost:3000?msg=token_expire")

        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        db.commit()

        return RedirectResponse(url="http://localhost:3000?msg=verified")

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

# ---------- Register Get Api ----------
@router.get('/getuser')
def get_user(current_user = Depends(get_current_user)  ):
    db = SessionLocal()

    user = db.query(User).filter(User.id == current_user.id).order_by(User.created_at.desc()).all()
    print("useruseruseruser" , user)

    if not user:
        raise HTTPException( 404 , "User not found" )
    return user

# ---------- Register update Api ----------

@router.put("/updateuser" , response_model=UserOut )
def update_user( payload:UserUpdate, background: BackgroundTasks , current_user= Depends(get_current_user) ):
    db = SessionLocal()

    user = db.query(User).filter(User.id == current_user.id).first()
    print("udpateuserudpateuserudpateuser" , user)

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    if payload.name is not None:
        user.name = payload.name
    
    if payload.address is not None:
        user.address = payload.address

    if payload.gender is not None:
        user.gender = payload.gender
    
    if payload.phone_number is not None:
        user.phone_number = payload.phone_number

    if payload.email is not None:
        user.email = payload.email
        user.is_verified = False

        token = secrets.token_urlsafe(32)
        user.verification_token = token
        user.verification_token_expires = datetime.utcnow() + timedelta(hours=1)

        # verification link
        verify_link = f"http://localhost:8000/auth/verify?token={token}"

        # mail bhejna
        background.add_task(
            send_email,
            to=user.email,
            subject="Verify your new email",
            body=f"Hi {user.name},\n\nPlease click the link to verify your new email:\n{verify_link}\n\nThis link expires in 1 hour."
        )
    db.commit()
    db.refresh(user)
    db.close()

    return UserOut.from_orm(user)

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

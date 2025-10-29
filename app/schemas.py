from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime


# ---------------- User Schemas ----------------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None

class UserCreatelogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_verified: bool   
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None       # ✅ add this field
    created_at: datetime

    class Config:
        from_attributes = True

class updatePassword(BaseModel):
    old_password: str
    new_password: str
    # confirm_password : str

# ---------------- Token Schema ----------------

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------------- Entry Schemas ----------------

class EntryCreate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    # status: Optional[Literal["active", "inactive"]] = "active"


class EntryOut(BaseModel):
    id: int
    owner_id: int
    title: str
    category: str
    content: str
    # status: str   # 👈 new
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------- Category Schemas ----------------

class categorySchema(BaseModel):
    category: str
    status: Optional[Literal["active", "inactive"]] = "active"


class categoryOut(BaseModel):
    id : int
    owner_id: int
    category: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------- Forget / Reset Password ----------------

class ForgetPassword(BaseModel):
    """Request body for the 'forgot password' endpoint."""
    email: EmailStr


class ResetPassword(BaseModel):
    """Request body for resetting the password."""
    token: str
    password: str
    

# ---------------- Email Verification ----------------

class VerifyEmailRequest(BaseModel):
    token: str      

class VerifyEmailResponse(BaseModel):
    message: str    



# ---------------- Attachment Schemas ----------------

# class AttachmentOut(BaseModel):
#     id: int
#     entry_id: int
#     filename: str
#     stored_name: str
#     mime_type: Optional[str]
#     size: Optional[int]
#     created_at: datetime

#     class Config:
#         from_attributes = True

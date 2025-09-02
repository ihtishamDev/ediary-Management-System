from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class EntryCreate(BaseModel):
    # id: int
    title: str
    content: str
    # class Config:
    #     from_attributes = True

class EntryOut(BaseModel):
    id: int
    owner_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class AttachmentOut(BaseModel):
    id: int
    entry_id: int
    filename: str
    stored_name: str
    mime_type: Optional[str]
    size: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True

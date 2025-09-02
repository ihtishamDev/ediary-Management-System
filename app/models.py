from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    entries = relationship('Entry', back_populates='owner')

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
    onupdate=func.now())
    owner = relationship('User', back_populates='entries')
    attachments = relationship('Attachment', back_populates='entry')

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey('entries.id'))
    filename = Column(String, nullable=False) # original filename
    stored_name = Column(String, nullable=False) # filename on disk
    mime_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    entry = relationship('Entry', back_populates='attachments')
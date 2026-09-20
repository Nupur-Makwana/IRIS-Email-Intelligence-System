# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 11:06:12 2026

@author: nupur
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)

    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)

    priority = Column(String(20), nullable=True)
    category = Column(String(50), nullable=True)
    summary = Column(Text, nullable=True)

    is_read = Column(Boolean, default=False)
    is_starred = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 12:00:01 2026

@author: nupur
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal
from models import User, Email
from ai import predict_priority
from security import get_current_user


router = APIRouter(
    prefix="/emails",
    tags=["Emails"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SendEmailRequest(BaseModel):
    receiver_email: str
    subject: str
    body: str


@router.post("/send")
def send_email(
    email_data: SendEmailRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    receiver = db.query(User).filter(
        User.email == email_data.receiver_email
    ).first()

    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="Receiver not found"
        )

    priority = predict_priority(
        email_data.subject,
        email_data.body
    )

    new_email = Email(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        subject=email_data.subject,
        body=email_data.body,
        priority=priority
    )

    db.add(new_email)
    db.commit()
    db.refresh(new_email)

    return {
        "message": "Email sent successfully",
        "email_id": new_email.id,
        "sender": current_user.email,
        "receiver": receiver.email,
        "subject": new_email.subject,
        "priority": new_email.priority
    }

@router.get("/inbox")
def get_inbox(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    emails = db.query(Email).filter(
        Email.receiver_id == current_user.id
    ).order_by(
        Email.created_at.desc()
    ).all()

    return {
        "user": current_user.email,
        "count": len(emails),
        "emails": [
            {
                "id": email.id,
                "sender_id": email.sender_id,
                "subject": email.subject,
                "body": email.body,
                "priority": email.priority,
                "category": email.category,
                "summary": email.summary,
                "is_read": email.is_read,
                "is_starred": email.is_starred,
                "created_at": email.created_at
            }
            for email in emails
        ]
    }


@router.get("/{email_id}")
def get_email(
    email_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = db.query(Email).filter(
        Email.id == email_id,
        Email.receiver_id == current_user.id
    ).first()

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    return {
        "id": email.id,
        "sender_id": email.sender_id,
        "receiver_id": email.receiver_id,
        "subject": email.subject,
        "body": email.body,
        "priority": email.priority,
        "category": email.category,
        "summary": email.summary,
        "is_read": email.is_read,
        "is_starred": email.is_starred,
        "created_at": email.created_at
    }

class ReadStatusRequest(BaseModel):
    is_read: bool


@router.patch("/{email_id}/read")
def update_read_status(
    email_id: int,
    status_data: ReadStatusRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = db.query(Email).filter(
        Email.id == email_id,
        Email.receiver_id == current_user.id
    ).first()

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    email.is_read = status_data.is_read

    db.commit()
    db.refresh(email)

    return {
        "message": "Email read status updated",
        "email_id": email.id,
        "is_read": email.is_read
    }
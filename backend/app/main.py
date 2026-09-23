# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 10:06:00 2026

@author: nupur
"""

from fastapi import FastAPI
from sqlalchemy import text

from database import engine, Base
from models import User, Email
from auth import router as auth_router
from emails import router as email_router

from pydantic import BaseModel
from ai import generate_summary

app = FastAPI(
    title="IRIS - Intelligent Email Analysis System",
    description="Backend API for the IRIS email intelligence system",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(email_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "IRIS Backend is running!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
def database_test():

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE();"))
            database_name = result.scalar()

        return {
            "status": "success",
            "database": database_name
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
class SummarizeRequest(BaseModel):
    subject: str
    body: str


@app.post("/ai/summarize")
def summarize_email_api(data: SummarizeRequest):
    summary = generate_summary(
        data.subject,
        data.body
    )

    return {
        "subject": data.subject,
        "summary": summary
    }
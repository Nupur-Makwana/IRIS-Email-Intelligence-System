# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 10:06:00 2026

@author: nupur
"""

from fastapi import FastAPI

app = FastAPI(
    title="IRIS - Intelligent Email Analysis System",
    description="Backend API for the IRIS email intelligence system",
    version="1.0.0"
)


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
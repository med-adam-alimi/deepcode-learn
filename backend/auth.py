# backend/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

# Simulated in-memory DB (replace with Firebase or DB later)
users_db: Dict[str, str] = {
    "test@test.com": "123456"  # ✅ Valid test user
}

class AuthRequest(BaseModel):
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

class ResetRequest(BaseModel):
    email: str

@router.post("/signup")
def signup(data: AuthRequest):
    if data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[data.email] = data.password
    return {"message": "✅ Signed up successfully"}

@router.post("/login")
def login(data: LoginData):
    if users_db.get(data.email) == data.password:
        return {"message": "✅ Login successful"}
    raise HTTPException(status_code=401, detail="❌ Invalid credentials")

@router.post("/reset-password")
def reset_password(data: ResetRequest):
    if data.email not in users_db:
        raise HTTPException(status_code=404, detail="Email not found")
    return {"message": "📧 Simulated password reset sent to your email"}

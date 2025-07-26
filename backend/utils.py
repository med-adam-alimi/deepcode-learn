from fastapi import Request, HTTPException
from firebase_admin import auth as firebase_auth

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No auth token")
    token = auth_header.split(" ")[1]
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print("❌ Invalid token:", e)
        raise HTTPException(status_code=403, detail="Invalid token")
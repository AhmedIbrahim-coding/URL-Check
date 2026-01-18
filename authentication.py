from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import bcrypt
import sqlite3, authorization
from schemas import UserLogin


router = APIRouter(
    tags=["Authentication"]
    )

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("select username, password from users where username = ?", (user_credentials.username,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")
    
    user_password = user_credentials.password.encode("utf-8")
    if not bcrypt.checkpw(user_password, row[1]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials!, Hashed{hashed_password}, correct{row[1]}")

    access_token = authorization.create_access_token(data={"username" : user_credentials.username})

    return {"access_token" : access_token}
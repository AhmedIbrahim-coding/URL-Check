from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
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
    
    if not row[1] == user_credentials.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")

    access_token = authorization.create_access_token(data={"username" : user_credentials.username})

    return {"access_token" : access_token}
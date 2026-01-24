from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import bcrypt
import sqlite3, authorization

# create the router app
router = APIRouter(
    tags=["Authentication"]
    )

# an endpoint to the user can login
@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends()): # get the credentials as (username , password) from the user request
    conn = sqlite3.connect("users.db")# connect to the local database 
    cursor = conn.cursor()

    # check if the user's username exists in the database or not
    cursor.execute("select username, password from users where username = ?", (user_credentials.username,))
    row = cursor.fetchone()
    cursor.close()# close the database connection

    # if the username doesn't exist, then return a 403 http excpetion with a massage
    if not row:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")
    
    # check if the username row includes a hashed password, then compare it with the sent password
    user_password = user_credentials.password.encode("utf-8")# hash the sent password to comparsion
    if not bcrypt.checkpw(user_password, row[1]):# check if two passwords are the same
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials!")

    # connect to the authorization file and use the create token function with the given payload
    access_token = authorization.create_access_token(data={"username" : user_credentials.username})

    # return an access point to the client to use it in any request 
    return {"access_token" : access_token}
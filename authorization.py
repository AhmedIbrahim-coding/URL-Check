from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime , timedelta
from fastapi import status, HTTPException
import os

# get the values required from the environment variables
SECRET_KEY = os.getenv("SEC", "fallback-secret-for-local-testing")
ALGORITH = os.getenv("ALG" ,"HS256")
EXPRIATION_TIME = int(os.getenv("EXPT", 20))

# Create a new token using the payload or the data & secret key & encoding algorithm
def create_access_token(data: dict):
    # take a copy of the original data dictionary
    to_encode = data.copy()

    # identify the expiration date that the token will be expred at
    expire = datetime.utcnow() + timedelta(minutes=EXPRIATION_TIME)
    to_encode.update({"exp" : expire})  # store the expiration date in the pyload with a new dict key

    # encode the data and create the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITH)

    return encoded_jwt


# Verify if the sent token is valid or not
def verify_access_token(token: str):
    try:
        # decode the sent token and extract the data or the payload
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITH])# The decoding won't happen if there is anything changed
        username = payload.get("username")  # get the username from the payload

        # if there isn't a username, it means the signature isn invalid
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    # if the token expireded then send a 401 http exception with a message
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
    # if there is any error appeared then send a 401 http exception with a message
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    

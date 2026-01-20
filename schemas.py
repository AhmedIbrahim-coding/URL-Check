from pydantic import BaseModel

# a Schema to hold the data when the user is trying to login
class UserLogin(BaseModel):
    username : str
    password : str

# a Schema to hold the access token & its type after creating it
class Token(BaseModel):
    access_token : str
    token_type : str

# a Schema to hold the token & url whenever the user is trying to check the url
class Values(BaseModel):
    url: str
    access_token: str

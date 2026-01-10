from fastapi import FastAPI
from pydantic import BaseModel

class Values(BaseModel):
    url : str

app = FastAPI()

@app.post("/")
def check_risk(values : Values):
    return {"message": f"Your link is {values.url}"}
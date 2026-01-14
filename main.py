from fastapi import FastAPI
from pydantic import BaseModel
from normalize import Normalizer

class Values(BaseModel):
    url: str

app = FastAPI()



@app.post("/")
def check_risk(values: Values):

    normalizer = Normalizer(values.url)

    url = normalizer.normalize_url()

    if not url:
        return {"message" : "not safe"}
    
    return {"url" : url}
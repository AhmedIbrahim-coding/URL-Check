from fastapi import FastAPI
from pydantic import BaseModel
from normalize import Normalizer
from authentication import router
import authorization
from schemas import Values


app = FastAPI()

app.include_router(router)


@app.post("/")
def check_risk(values: Values):

    authorization.verify_access_token(values.access_token)

    
    normalizer = Normalizer(values.url)

    url = normalizer.normalize_url()

    if not url:
        return {"message" : "not safe"}
    
    return {"url" : url}


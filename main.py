from fastapi import FastAPI
from normalize import Normalizer
from local_validate import Validator
from authentication import router
import authorization
from schemas import Values


app = FastAPI()

app.include_router(router)


@app.post("/check")
def check_risk(values: Values):
    url = values.url

    authorization.verify_access_token(values.access_token)

    # Start normalizing the url
    normalizer = Normalizer(url)
    url = normalizer.normalize_url()

    if not url:
        return {"message" : "not safe"}
    
    # Validate the url
    validator = Validator(url)
    valid = validator.is_valid()

    if not valid:
        return {"message" : "not safe"}
    
    return {"url" : url}


from fastapi import FastAPI
from normalize import Normalizer
from local_validate import Validator
from authentication import router
import authorization
from schemas import Values

# create the API app
app = FastAPI()

# include the authentication router
app.include_router(router)


# an endpoint for checking the url that takes the url and the access token
@app.post("/check")
def check_risk(values: Values):
    url = values.url

    # make sure that the request includes a valid access token first
    authorization.verify_access_token(values.access_token)

    # Start normalizing the url
    normalizer = Normalizer(url)
    url = normalizer.normalize_url()

    # return a "not safe" message for the user if the url wasn't returned
    if not url:
        return {"message" : "not safe"}
    
    # Validate the url
    validator = Validator(url)
    valid = validator.is_valid()

    # return a "not safe" message for the user if the url isn't valid locally
    if not valid:
        return {"message" : "not safe"}
    
    
    return {"url" : url}


from fastapi import FastAPI
from normalize import Normalizer
from local_validate import Validator
from authentication import router
import authorization, reputation
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
    
    
    # check the reputation with VirusTotal api
    try:        
        stats = reputation.get_stats(url)   # get the result
        malicious = stats.get("malicious", 0)
        total_engines = sum(stats.values()) 
    except:
        return {"message" : "Unknown"}

    # the engines are supposed to be 95 if it's 0 then there is a problem
    if total_engines == 0:
        return {"message" : "Unkown"}
    
    # clac the ration
    ratio = malicious / total_engines

    if malicious >= 3 or ratio > 0.05:
        return {"message" : "not safe"}    
    elif malicious > 0:
        return {"mesage" : "Propaply clean"}
    else:
        return {"message" : "Clean"}


from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse

class Values(BaseModel):
    url : str

app = FastAPI()

# for nomalizing the data
def normalize_url(url : str):
    url = url.strip()

    # ensure the url isn't a whitespace
    if not url:
        return None
    
    # ensure the url is in small characters
    url = url.lower()

    # ensure the scheme exists
    if not url.startswith(("https://" , "http://")):
        url = "https://" + url

    # return the final normalized url
    return url

# convert the url into components
def parse_url(url : str) -> dict:
    parsed = urlparse(url=url)

    return {
        "scheme" : parsed.scheme,
        "netloc" : parsed.netloc,
        "hostname" : parsed.hostname,
        "port" : parsed.port,
        "path" : parsed.path,
        "query" : parsed.query,
        "fragment" : parsed.fragment
    }

@app.post("/")
def check_risk(values : Values):

    # operate the normalization func
    url = normalize_url(values.url)
    
    # continue only if a url is returned
    if not url:
        return {"message" : "None"}
    
    # operate the url parsing
    url = parse_url(url)
    
    # return the returned url dict
    return url
    
    

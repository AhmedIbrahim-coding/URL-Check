from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse, ParseResult
import idna
import ipaddress
import re

class Values(BaseModel):
    url: str

app = FastAPI()


def normalize_url(url: str):
    url = url.strip()
    if not url:
        return None
    return url

def ensure_scheme(url : str) -> str:
    parsed = urlparse(url)

    if "://" in url:
        return url

    if re.fullmatch(r"[a-zA-Z0-9.-]+:\d{1,5}", url):
        return "https://" + url

    if parsed.scheme:
        return url
    
    return "https://" + url


def validate_scheme(parsed: ParseResult) -> ParseResult:
    allowed_schemes = {"http", "https"}
    scheme = parsed.scheme.lower() if parsed.scheme else "https"

    if scheme not in allowed_schemes:
        raise Exception("Unsupported scheme")

    return parsed._replace(scheme=scheme)

def validate_hostname(parsed: ParseResult) -> ParseResult:
    hostname = parsed.hostname
    if not hostname:
        raise Exception("Missing hostname")

    hostname = hostname.lower().rstrip(".")

    try:
        ipaddress.ip_address(hostname)
        normalized_host = hostname
    except ValueError:
        normalized_host = idna.encode(hostname).decode("ascii")

    return parsed._replace(netloc=normalized_host)

def normalize_port(parsed: ParseResult) -> ParseResult:
    # store the port & the scheme in variables
    port = parsed.port
    scheme = parsed.scheme

    # just continue if the port exists if it's not return immediatly 
    if port == None:
        return parsed

    # raise an error if the port doesn't follow the port range rule
    if not (1 <= port <= 65535):
        raise Exception

    # put default port numbers for both http & https
    default_ports = {
        "https" : 443,
        "http" : 80,
    }

    # get the hostname, username(auth), and password(auth) form the url
    hostname = parsed.hostname
    username = parsed.username
    password = parsed.password

    # check if there is an (RFC 3986) authentication in the URL
    auth = ""
    if username:
        auth = username
        if password:
            auth += f":{password}"
        auth += "@"

    # if the port is deafult to the scheme remove it is it not keep it
    if port == default_ports.get(scheme):
        netloc = f"{auth}{hostname}"
    else:
        netloc = f"{auth}{hostname}:{port}"

    # replace the old netlock with the new built netloc
    return parsed._replace(netloc=netloc)



@app.post("/")
def check_risk(values: Values):
    url = normalize_url(values.url)
    if not url:
        return {"message": "empty url"}

    # ensure the scheme exists before parsing
    url = ensure_scheme(url)

    try:
        parsed = urlparse(url)
        parsed = validate_scheme(parsed)
        parsed = validate_hostname(parsed)
        parsed = normalize_port(parsed)

    except Exception:
        return {"message": "not safe"}

    return {
        "scheme": parsed.scheme,
        "hostname": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "query": parsed.query,
    }

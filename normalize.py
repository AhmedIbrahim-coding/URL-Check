from urllib.parse import urlparse, ParseResult, urlunparse
import idna
import ipaddress
import re


class Normalizer:
    def __init__(self, url):
        self.url = url

    
    def normalize_url(self) -> str:
        url = self.url.strip()
        if not url:
            return None
        
        # ensure the scheme exists before parsing
        url = self.ensure_scheme(url)

        # try all the functions
        try:
            parsed = urlparse(url)
            parsed = self.validate_scheme(parsed)
            parsed = self.validate_hostname(parsed)
            parsed = self.normalize_port(parsed)
            parsed = self.remove_fragment(parsed)
            url = urlunparse(parsed)
        # if there is any exception then return a None value
        except Exception:
            return None
        
        # if the url passes with all the these functions then return the normalized url
        return url

    def ensure_scheme(self, url : str) -> str:
        parsed = urlparse(url)# extract the url into components

        # if there is a scheme suffex then it contains the scheme
        if "://" in url:
            return url

        # if the url doesn't contain a sheme then add it before the url
        if re.fullmatch(r"[a-zA-Z0-9.-]+:\d{1,5}", url):
            return "https://" + url

        if parsed.scheme:
            return url
        
        # finally return the url with a scheme in the beginning
        return "https://" + url
    
    
    def validate_scheme(self, parsed: ParseResult) -> ParseResult:
        # make sure the url includes an allowed scheme
        allowed_schemes = {"http", "https"}
        scheme = parsed.scheme.lower() if parsed.scheme else "https"

        if scheme not in allowed_schemes:
            raise Exception("Unsupported scheme")

        return parsed._replace(scheme=scheme)


    def validate_hostname(self, parsed: ParseResult) -> ParseResult:
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

    

    def normalize_port(self, parsed: ParseResult) -> ParseResult:
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
    
    def remove_fragment(self, parsed : ParseResult) -> ParseResult:
        # get the fragments and remove then all
        frag = parsed.fragment
        if not frag:
            return parsed

        return parsed._replace(fragment="")


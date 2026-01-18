import re
import tldextract
from urllib.parse import urlparse, urlunparse
import ipaddress

class Validator:
    def __init__(self, url):
        self.url = url

    def is_valid(self) -> bool:
        url = self.url

        if len(url) > 2048:
            return False
        
        if not self.validate_syntax(url):
            return False
        
        if not self.is_valid_domain(url):
            return False

        return True

    def validate_syntax(self, url) -> bool:

        pattern = re.compile(
            r'^https?://'                     # Scheme
            r'(?:[a-zA-Z0-9-._~%]+@)?'       # Userinfo (optional)
            r'(?:[a-zA-Z0-9.-]+|\[[a-fA-F0-9:]+\])' # Host (Domain or IPv6)
            r'(?::\d+)?'                     # Port (optional)
            r'(?:/[a-zA-Z0-9-._~%!$&\'()*+,;=:@/]*)?' # Path
            r'(?:\?[a-zA-Z0-9-._~%!$&\'()*+,;=:@/?]*)?$', # Query
            re.IGNORECASE     
        )
        
        return bool(pattern.match(url))
    
    def is_valid_domain(self, url : str) -> bool:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if not hostname:
            return False

        try:
            ip = ipaddress.ip_address(hostname)

            return ip.is_global
        except ValueError:
            extracted = tldextract.extract(url)
            return bool(extracted.domain and extracted.suffix)
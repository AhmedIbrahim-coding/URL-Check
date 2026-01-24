import re
import tldextract
from urllib.parse import urlparse
import ipaddress

# a validator to make sure that the url is (locally) valid or not
class Validator:
    def __init__(self, url):
        self.url = url

    # a one function to call all the function
    def is_valid(self) -> bool:
        url = self.url

        # make sure that the url's lenght is less than 2048 character
        if len(url) > 2048:
            return False
        
        # check the url syntax
        if not self.validate_syntax(url):
            return False
        
        # check the url domain
        if not self.is_valid_domain(url):
            return False

        # if it passes all the checks and didn't return false then return true
        return True

    def validate_syntax(self, url) -> bool:

        # store the standard url pattern
        pattern = re.compile(
            r'^https?://'                     # Scheme
            r'(?:[a-zA-Z0-9-._~%]+@)?'       # Userinfo (optional)
            r'(?:[a-zA-Z0-9.-]+|\[[a-fA-F0-9:]+\])' # Host (Domain or IPv6)
            r'(?::\d+)?'                     # Port (optional)
            r'(?:/[a-zA-Z0-9-._~%!$&\'()*+,;=:@/]*)?' # Path
            r'(?:\?[a-zA-Z0-9-._~%!$&\'()*+,;=:@/?]*)?$', # Query
            re.IGNORECASE   # to ignore if it's lowercase or uppercase  
        )
        
        # return a boolen value wether the url mathes the standard pattern or it doesn't
        return bool(pattern.match(url))
    

    def is_valid_domain(self, url : str) -> bool:
        # first parse the url and get the host name
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        # if the host name doesn't exist then return false
        if not hostname:
            return False

        # if the url is ip adress then make sure that it's global not a private ip
        try:
            ip = ipaddress.ip_address(hostname)

            return ip.is_global
        # if it's not an ip adress it means it's a domain
        except ValueError:
            # extract the domain name and the suffix and make sure that they exist
            extracted = tldextract.extract(url)
            return bool(extracted.domain and extracted.suffix)
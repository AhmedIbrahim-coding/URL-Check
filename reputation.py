import requests
import base64

virus_total_key = "079e7277985160636159bf95c0d42fb83f59438cfac09ba7dbd4e97af65559b5"

def get_stats(url_toCheck: str) -> dict:
    url_id = base64.urlsafe_b64encode(url_toCheck.encode()).decode().strip("=")

    url = f"https://www.virustotal.com/api/v3/urls/{url_id}"

    headers = {
        "accept": "application/json",
        "x-apikey": virus_total_key
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]
        return stats
    else:
        raise Exception
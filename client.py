import requests

link = input("Enter URL: ")

pack = {"url" : link}

response = requests.post(url="http://127.0.0.1:8000", json=pack)
content = response.json()


if "message" in content:
    print(content["message"])
else:
    print((content))
import requests

link = input("Enter URL: ")

pack = {"url" : link}

response = requests.post(url="https://127.0.0.1:8000", json=pack)
print(response.content)
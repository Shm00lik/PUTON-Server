import requests

url = "http://localhost:3339/register"

payload = {"username": "testUn", "password": "testPass"}

r = requests.post(url, data=payload)
print(r.text)

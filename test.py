import requests
from config import API_KEY

url = "https://api.air.fail/public/text/"
headers = {"Authorization": API_KEY}
data = {"email": "sergomet.225@gmail.com", "password": "Programmist5742"}
response = requests.get(url, headers=headers)
print(response.json())
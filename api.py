import requests
from config import API_KEY, API_KEY_IMAGE


def gpt(text):
 url = "https://api.air.fail/public/text/chatgpt"
 headers= {"Authorization": API_KEY}
 data = {"model":"gpt-4", "content": "Привет!","info":{"temperature": 0.5}}
 response = requests.post(url,json=data,headers=headers)
 return response.json()[0]["content"]

def image(text):
 url = "https://api.air.fail/public/image/stablediffision"
 headers= {"Authorization": API_KEY_IMAGE}
 data = { "content": text}
 response = requests.post(url,json=data,headers=headers)
 return response.json()[0]["file"],response.json()[1]["content"]
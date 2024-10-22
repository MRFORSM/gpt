import requests
url = "https://api.air.fail/public/image/stablediffision"
headers= {"Authorization": API_KEY_IMAGE}
response = requests.post(url,json=data,headers=headers)
print(response.json())
import requests
import json

url = "http://api.bilibili.com/x/web-interface/view?aid=82332361"
resp = requests.get(url).json()
print(resp["message"])

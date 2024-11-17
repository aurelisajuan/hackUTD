import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()
url = "https://api.pinata.cloud/v3/files"
db_id = 'bafkreiav6jiqlcgtv3vdbzz57qvin5xrt6zpez64vk3i2psxezgwvjx6ym'

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['PINATA_JWT']}"
}

def fetch_files():
    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_db():
  payload = {
    "url": f"{os.environ['GATEWAY_URL']}/files/{db_id}",
    "date": int(time.time()),
    "expires": 30,
    "method": "GET"
  }
  response = requests.request("POST", url=f"{url}/sign", json=payload, headers=headers)
  file_url = response.json()['data']
  
  return requests.request("GET", file_url, headers=headers).json()


print(get_db())
# print(fetch_files())


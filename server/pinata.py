import requests
import os
from dotenv import load_dotenv
load_dotenv()
url = "https://api.pinata.cloud/v3/files"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['PINATA_JWT']}"
}


def fetch_latest_statement():
    response = requests.request("GET", url, headers=headers)
    return response.json()

print(fetch_latest_statement())
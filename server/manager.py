import requests
import os
import time
import json


def get_account_info():
    account_id = "ACC123"
    with open('db.json', 'r') as f:
        db = json.load(f)
    account_info = db["accounts"].get(account_id, {})
    return account_info

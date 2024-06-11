import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_delegators(receiver_account):
    url = f"https://ecency.com/private-api/received-vesting/{receiver_account}"
    response = requests.get(url)
    data = response.json()
    return data['list']

def fetch_delegators():
    receiver_account = os.getenv("RECEIVER_ACCOUNT")
    return get_delegators(receiver_account)

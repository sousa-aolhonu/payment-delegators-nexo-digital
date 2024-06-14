import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def get_delegators(receiver_account):
    try:
        url = f"https://ecency.com/private-api/received-vesting/{receiver_account}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['list']
    except requests.exceptions.RequestException as e:
        print(f"[Error] Error fetching delegators: {e}")
        return []
    except KeyError as e:
        print(f"[Error] Unexpected response format: {e}")
        return []

def fetch_delegators():
    try:
        receiver_account = os.getenv("RECEIVER_ACCOUNT")
        if not receiver_account:
            raise ValueError("[Error] RECEIVER_ACCOUNT is not set in the environment variables.")
        print(f"[Info] Fetching delegators for {receiver_account}...")
        delegators = get_delegators(receiver_account)
        print(f"[Success] Fetched delegators successfully.")
        return delegators
    except Exception as e:
        print(f"[Error] Error in fetch_delegators: {e}")
        return []

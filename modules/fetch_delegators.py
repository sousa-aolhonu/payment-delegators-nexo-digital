import requests
from dotenv import load_dotenv
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

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
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error fetching delegators: {e}")
        return []
    except KeyError as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Unexpected response format: {e}")
        return []

def fetch_delegators():
    try:
        receiver_account = os.getenv("RECEIVER_ACCOUNT")
        if not receiver_account:
            raise ValueError(f"{Fore.RED}[Error]{Style.RESET_ALL} RECEIVER_ACCOUNT is not set in the environment variables.")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching delegators for {Fore.BLUE}{receiver_account}{Style.RESET_ALL}...")
        delegators = get_delegators(receiver_account)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Fetched delegators successfully.")
        return delegators
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error in fetch_delegators: {e}")
        return []

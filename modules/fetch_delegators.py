import requests
import logging
from dotenv import load_dotenv
import os
from colorama import Fore, Style, init

init(autoreset=True)

load_dotenv()

def get_delegators(receiver_account):
    endpoints = [
        f"https://peakd.com/api/public/delegations/incoming?delegatee={receiver_account}",
        f"https://ecency.com/private-api/received-vesting/{receiver_account}",
        f"https://api.hive-keychain.com/hive/delegators/{receiver_account}"
    ]

    for url in endpoints:
        try:
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching delegators for {Fore.BLUE}{receiver_account}{Style.RESET_ALL} from {url}...")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "peakd" in url:
                delegators = [{"delegator": item["delegator"], "vesting_shares": float(item["vests"])} for item in data]
            elif "ecency" in url:
                delegators = [{"delegator": item["delegator"], "vesting_shares": float(item["vesting_shares"].replace(' VESTS', ''))} for item in data['list']]
            elif "hive-keychain" in url:
                delegators = [{"delegator": item["delegator"], "vesting_shares": item["vesting_shares"]} for item in data]
                delegators = [item for item in delegators if item["vesting_shares"] > 0]

            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Delegators fetched successfully from {url}.")
            return delegators
        except Exception as e:
            logging.error(f"Error fetching delegators from {url}: {e}")
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error fetching delegators from {url}: {e}")

    return []

def fetch_delegators():
    try:
        receiver_account = os.getenv("RECEIVER_ACCOUNT")
        if not receiver_account:
            raise ValueError(f"{Fore.RED}[Error]{Style.RESET_ALL} RECEIVER_ACCOUNT is not set in the environment variables.")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching delegators for {Fore.BLUE}{receiver_account}{Style.RESET_ALL}...")
        delegators = get_delegators(receiver_account)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Delegators fetched successfully.")
        return delegators
    except Exception as e:
        logging.error(f"Error in fetch_delegators: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error in fetch_delegators: {e}")
        return []

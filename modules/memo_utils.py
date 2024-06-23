import os
import hashlib
import logging
import requests
from datetime import datetime
from colorama import Fore, Style

def generate_unique_hash(account, amount, date):
    try:
        data = f"{account}{amount}{date}"
        return hashlib.sha256(data.encode()).hexdigest()
    except Exception as e:
        logging.error(f"Error generating unique hash: {e}")
        return None

def format_memo(account, amount, date, unique_hash):
    try:
        return f"Reward for Hive Power delegation from {account} to {os.getenv('RECEIVER_ACCOUNT')} of {amount} NEXO on {date}. Hash: {unique_hash}"
    except Exception as e:
        logging.error(f"Error formatting memo: {e}")
        return None

def get_current_date():
    try:
        return datetime.now().strftime("%Y-%m-%d")
    except Exception as e:
        logging.error(f"Error getting current date: {e}")
        return None

def memo_exists(payment_account, memo, token_name):
    try:
        logging.info(f"Checking for existing memo: {memo}")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Checking for existing memo: {memo}")
        url = f"https://history.hive-engine.com/accountHistory?account={payment_account}&limit=100&symbol={token_name}"
        response = requests.get(url)
        response.raise_for_status()
        transactions = response.json()
        for transaction in transactions:
            if transaction.get('memo') == memo:
                logging.warning(f"Memo already exists in transaction history: {memo}")
                print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} Memo already exists in transaction history: {memo}")
                return True
        return False
    except Exception as e:
        logging.error(f"Error checking for existing memo: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error checking for existing memo: {e}")
        return False

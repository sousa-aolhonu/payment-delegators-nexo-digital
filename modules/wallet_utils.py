import time
import logging
from colorama import Fore, Style
from beem import Hive
from beem.account import Account
from hiveengine.wallet import Wallet as HiveEngineWallet
from dotenv import load_dotenv
import os

load_dotenv()

def check_balance(wallet):
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Checking balance...")
        balances = wallet.get_balances()
        nexo_balance = next((item["balance"] for item in balances if item["symbol"] == "NEXO"), 0.0)
        nexo_balance = float(nexo_balance)
        nexo_balance = round(nexo_balance, 3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} NEXO balance retrieved: {Fore.YELLOW}{nexo_balance}{Style.RESET_ALL}")
        return nexo_balance
    except Exception as e:
        logging.error(f"Error checking NEXO balance: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error checking NEXO balance: {e}")
        return 0.0

def wait_for_transaction(wallet, initial_balance, payment_amount, max_attempts=1000, wait_time=10):
    attempts = 0
    while attempts < max_attempts:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Waiting for {wait_time} seconds before checking transaction...")
        time.sleep(wait_time)
        current_balance = check_balance(wallet)
        expected_balance = round(initial_balance - payment_amount, 3)
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Checking if transaction is reflected in the blockchain. Attempt {attempts + 1}/{max_attempts}")
        if current_balance == expected_balance:
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Transaction reflected in the blockchain. Current balance: {Fore.YELLOW}{current_balance}{Style.RESET_ALL}")
            return current_balance
        attempts += 1
    logging.error(f"Transaction not reflected after {max_attempts} attempts.")
    print(f"{Fore.RED}[Error]{Style.RESET_ALL} Transaction not reflected after {max_attempts} attempts.")
    return None

def wait_for_transaction_id(payment_account, delegator, payment_amount, token_name, max_attempts=1000, wait_time=10):
    from modules.transaction import get_transaction_id

    attempts = 0
    while attempts < max_attempts:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Waiting for {wait_time} seconds before fetching transaction ID...")
        time.sleep(wait_time)
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching transaction ID. Attempt {attempts + 1}/{max_attempts}")
        txid = get_transaction_id(payment_account, delegator, payment_amount, token_name)
        if txid:
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Transaction ID retrieved: {Fore.YELLOW}{txid}{Style.RESET_ALL}")
            return txid
        attempts += 1
    logging.error(f"Transaction ID not found after {max_attempts} attempts.")
    print(f"{Fore.RED}[Error]{Style.RESET_ALL} Transaction ID not found after {max_attempts} attempts.")
    return None

def configure_hive():
    try:
        logging.info("Configuring Hive...")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Configuring Hive...")
        stm = Hive(node="https://api.hive.blog", keys=[os.getenv("HIVE_ENGINE_ACTIVE_PRIVATE_KEY"), os.getenv("HIVE_ENGINE_POSTING_PRIVATE_KEY")])
        account = Account(os.getenv("PAYMENT_ACCOUNT"), blockchain_instance=stm)
        logging.info("Hive configured successfully.")
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Hive configured successfully.")
        return stm, account
    except Exception as e:
        logging.error(f"Error configuring Hive: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error configuring Hive: {e}")
        return None, None

def configure_hive_engine_wallet(account, stm):
    try:
        logging.info("Configuring Hive Engine Wallet...")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Configuring Hive Engine Wallet...")
        wallet = HiveEngineWallet(account.name, steem_instance=stm)
        logging.info("Hive Engine Wallet configured successfully.")
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Hive Engine Wallet configured successfully.")
        return wallet
    except Exception as e:
        logging.error(f"Error configuring Hive Engine Wallet: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error configuring Hive Engine Wallet: {e}")
        return None

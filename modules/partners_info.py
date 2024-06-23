from dotenv import load_dotenv
import os
import logging
from colorama import Fore, Style, init

init(autoreset=True)

load_dotenv()

def get_partner_accounts():
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching partner accounts...")
        logging.info("Fetching partner accounts...")
        partner_accounts = os.getenv("PARTNER_ACCOUNTS")
        if partner_accounts:
            accounts = partner_accounts.split(',')
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Partner accounts retrieved: {Fore.YELLOW}{accounts}")
            logging.info(f"Partner accounts retrieved: {accounts}")
            return accounts
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No partner accounts set.")
        logging.info("No partner accounts set.")
        return []
    except Exception as e:
        logging.error(f"Error getting partner accounts: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting partner accounts: {e}")
        return []

def get_ignore_payment_accounts():
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching ignore payment accounts...")
        logging.info("Fetching ignore payment accounts...")
        ignore_payment_accounts = os.getenv("IGNORE_PAYMENT_ACCOUNTS")
        if ignore_payment_accounts:
            accounts = ignore_payment_accounts.split(',')
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Ignore payment accounts retrieved: {Fore.YELLOW}{accounts}")
            logging.info(f"Ignore payment accounts retrieved: {accounts}")
            return accounts
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No ignore payment accounts set.")
        logging.info("No ignore payment accounts set.")
        return []
    except Exception as e:
        logging.error(f"Error getting ignore payment accounts: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting ignore payment accounts: {e}")
        return []

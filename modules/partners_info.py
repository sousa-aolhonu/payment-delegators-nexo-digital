from dotenv import load_dotenv
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

load_dotenv()

def get_partner_accounts():
    try:
        partner_accounts = os.getenv("PARTNER_ACCOUNTS")
        if partner_accounts:
            accounts = partner_accounts.split(',')
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Partner accounts retrieved.")
            return accounts
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No partner accounts set.")
        return []
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting partner accounts: {e}")
        return []

def get_ignore_payment_accounts():
    try:
        ignore_payment_accounts = os.getenv("IGNORE_PAYMENT_ACCOUNTS")
        if ignore_payment_accounts:
            accounts = ignore_payment_accounts.split(',')
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Ignore payment accounts retrieved.")
            return accounts
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No ignore payment accounts set.")
        return []
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting ignore payment accounts: {e}")
        return []

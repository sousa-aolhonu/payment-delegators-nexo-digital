import time
from colorama import Fore, Style

def check_balance(wallet):
    try:
        balances = wallet.get_balances()
        nexo_balance = next((item["balance"] for item in balances if item["symbol"] == "NEXO"), 0.0)
        nexo_balance = float(nexo_balance)  # Garantir que seja float antes de arredondar
        nexo_balance = round(nexo_balance, 3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} NEXO balance retrieved: {Fore.YELLOW}{nexo_balance}{Style.RESET_ALL}")
        return nexo_balance
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error checking NEXO balance: {e}")
        return 0.0

def wait_for_transaction(wallet, initial_balance, payment_amount, max_attempts=1000, wait_time=1):
    attempts = 0
    while attempts < max_attempts:
        time.sleep(wait_time)
        current_balance = check_balance(wallet)
        expected_balance = round(initial_balance - payment_amount, 3)
        if current_balance == expected_balance:
            return current_balance
        attempts += 1
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Waiting for transaction to be reflected in the blockchain... Attempt {attempts}/{max_attempts}")
    print(f"{Fore.RED}[Error]{Style.RESET_ALL} Transaction not reflected after {max_attempts} attempts.")
    return None

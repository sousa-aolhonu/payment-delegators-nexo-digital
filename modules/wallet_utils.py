import time
from colorama import Fore, Style

def check_balance(wallet):
    """
    Checks the balance of the wallet for the NEXO token.

    Args:
        wallet (HiveEngineWallet): The Hive Engine wallet to check the balance of.

    Returns:
        float: The NEXO balance, or 0.0 if an error occurs.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Checking balance...")
        balances = wallet.get_balances()
        nexo_balance = next((item["balance"] for item in balances if item["symbol"] == "NEXO"), 0.0)
        nexo_balance = float(nexo_balance)  # Garantir que seja float antes de arredondar
        nexo_balance = round(nexo_balance, 3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} NEXO balance retrieved: {Fore.YELLOW}{nexo_balance}{Style.RESET_ALL}")
        return nexo_balance
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error checking NEXO balance: {e}")
        return 0.0

def wait_for_transaction(wallet, initial_balance, payment_amount, max_attempts=1000, wait_time=10):
    """
    Waits for a transaction to be reflected in the blockchain.

    Args:
        wallet (HiveEngineWallet): The Hive Engine wallet to check the balance of.
        initial_balance (float): The initial balance before the transaction.
        payment_amount (float): The amount of the payment.
        max_attempts (int, optional): The maximum number of attempts to check for the transaction. Defaults to 1000.
        wait_time (int, optional): The time to wait between attempts, in seconds. Defaults to 10.

    Returns:
        float: The final balance if the transaction is reflected, None otherwise.
    """
    attempts = 0
    while attempts < max_attempts:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Waiting for {wait_time} seconds before checking transaction...")
        time.sleep(wait_time)
        current_balance = check_balance(wallet)
        expected_balance = round(initial_balance - payment_amount, 3)
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Checking if transaction is reflected in the blockchain. Attempt {attempts + 1}/{max_attempts}")
        if current_balance == expected_balance:
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Transaction reflected in the blockchain. Current balance: {Fore.YELLOW}{current_balance}")
            return current_balance
        attempts += 1
    print(f"{Fore.RED}[Error]{Style.RESET_ALL} Transaction not reflected after {max_attempts} attempts.")
    return None

def wait_for_transaction_id(payment_account, delegator, payment_amount, token_name, max_attempts=1000, wait_time=10):
    """
    Waits for the transaction ID to be available on the blockchain.

    Args:
        payment_account (str): The account making the payment.
        delegator (str): The account receiving the payment.
        payment_amount (float): The amount of the payment.
        token_name (str): The name of the token paid.
        max_attempts (int, optional): The maximum number of attempts to check for the transaction ID. Defaults to 1000.
        wait_time (int, optional): The time to wait between attempts, in seconds. Defaults to 10.

    Returns:
        str: The transaction ID if found, None otherwise.
    """
    from modules.transaction import get_transaction_id  # Importar aqui para evitar importação circular

    attempts = 0
    while attempts < max_attempts:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Waiting for {wait_time} seconds before fetching transaction ID...")
        time.sleep(wait_time)
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching transaction ID. Attempt {attempts + 1}/{max_attempts}")
        txid = get_transaction_id(payment_account, delegator, payment_amount, token_name)
        if txid:
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Transaction ID retrieved: {Fore.YELLOW}{txid}")
            return txid
        attempts += 1
    print(f"{Fore.RED}[Error]{Style.RESET_ALL} Transaction ID not found after {max_attempts} attempts.")
    return None

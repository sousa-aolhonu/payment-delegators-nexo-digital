import requests
from colorama import Fore, Style

def get_transaction_id(payment_account, delegator, payment_amount, token_name):
    """
    Fetches the transaction ID for a payment from the payment account to the delegator.

    Args:
        payment_account (str): The account making the payment.
        delegator (str): The account receiving the payment.
        payment_amount (float): The amount of tokens paid.
        token_name (str): The name of the token paid.

    Returns:
        str: The transaction ID if found, None otherwise.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching transaction ID for payment from {Fore.BLUE}{payment_account}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL}...")
        url = f"https://history.hive-engine.com/accountHistory?account={payment_account}&limit=30&offset=0&symbol={token_name}"
        response = requests.get(url)
        response.raise_for_status()
        transactions = response.json()
        
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Filtering transactions for the correct one...")
        for transaction in transactions:
            if (transaction['from'] == payment_account and 
                transaction['to'] == delegator and 
                float(transaction['quantity']) == payment_amount):
                print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Transaction ID found: {Fore.YELLOW}{transaction['transactionId']}")
                return transaction['transactionId']
        
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Transaction ID not found for payment from {Fore.BLUE}{payment_account}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error fetching transaction ID: {e}")
        return None

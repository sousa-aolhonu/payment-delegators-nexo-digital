import requests
from dotenv import load_dotenv
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

load_dotenv()

def get_transaction_id(payment_account, to_account, amount, token_name):
    try:
        url = f"https://history.hive-engine.com/accountHistory?account={payment_account}&limit=30&offset=0&symbol={token_name}"
        response = requests.get(url)
        response.raise_for_status()
        transactions = response.json()

        for transaction in transactions:
            if (transaction.get("from") == payment_account and
                transaction.get("to") == to_account and
                float(transaction.get("quantity", 0)) == amount):
                return transaction.get("transactionId")

        print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} Transaction ID not found for payment to {Fore.BLUE}{to_account}{Style.RESET_ALL}.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error fetching transaction ID: {e}")
        return None

# Example usage
if __name__ == "__main__":
    payment_account = "nexo.pool"
    to_account = "someaccount"
    amount = 5.82
    token_name = "NEXO"
    txid = get_transaction_id(payment_account, to_account, amount, token_name)
    print(f"Transaction ID: {txid}")

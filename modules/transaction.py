import requests
import logging
from colorama import Fore, Style


def get_transaction_id(payment_account, delegator, payment_amount, token_name):
    try:
        print(
            f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching transaction ID for payment from {Fore.BLUE}{payment_account}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL}..."
        )
        url = f"https://history.hive-engine.com/accountHistory?account={payment_account}&limit=30&offset=0&symbol={token_name}"
        response = requests.get(url)
        response.raise_for_status()
        transactions = response.json()

        print(
            f"{Fore.CYAN}[Info]{Style.RESET_ALL} Filtering transactions for the correct one..."
        )
        for transaction in transactions:
            if (
                transaction["from"] == payment_account
                and transaction["to"] == delegator
                and float(transaction["quantity"]) == payment_amount
            ):
                print(
                    f"{Fore.GREEN}[Success]{Style.RESET_ALL} Transaction ID found: {Fore.YELLOW}{transaction['transactionId']}"
                )
                return transaction["transactionId"]

        print(
            f"{Fore.RED}[Error]{Style.RESET_ALL} Transaction ID not found for payment from {Fore.BLUE}{payment_account}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL}"
        )
        return None
    except Exception as e:
        logging.error(f"Error fetching transaction ID: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error fetching transaction ID: {e}")
        return None

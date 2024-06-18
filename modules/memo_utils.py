import os
import hashlib
from datetime import datetime

def generate_unique_hash(account, amount, date):
    """
    Generates a unique hash based on the account, amount, and date.

    Args:
        account (str): The account name.
        amount (float): The payment amount.
        date (str): The date of the payment.

    Returns:
        str: The unique hash.
    """
    data = f"{account}{amount}{date}"
    return hashlib.sha256(data.encode()).hexdigest()

def format_memo(account, amount, date, unique_hash):
    """
    Formats the memo message for the transaction.

    Args:
        account (str): The account name.
        amount (float): The payment amount.
        date (str): The date of the payment.
        unique_hash (str): The unique hash for the transaction.

    Returns:
        str: The formatted memo message.
    """
    return f"Reward for Hive Power delegation from {account} to {os.getenv('RECEIVER_ACCOUNT')} of {amount} NEXO on {date}. Hash: {unique_hash}"

def get_current_date():
    """
    Gets the current date in the format YYYY-MM-DD.

    Returns:
        str: The current date.
    """
    return datetime.now().strftime("%Y-%m-%d")

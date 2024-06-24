import os
import hashlib
import logging
from datetime import datetime

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

import os
import hashlib
from datetime import datetime


def generate_unique_hash(account, amount, date):
    data = f"{account}{amount}{date}"
    return hashlib.sha256(data.encode()).hexdigest()


def format_memo(account, amount, date, unique_hash):
    return f"Reward for Hive Power delegation from {account} to {os.getenv('RECEIVER_ACCOUNT')} of {amount} NEXO on {date}. Hash: {unique_hash}"


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

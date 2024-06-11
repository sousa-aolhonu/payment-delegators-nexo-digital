from dotenv import load_dotenv
import os

load_dotenv()

def get_partner_accounts():
    partner_accounts = os.getenv("PARTNER_ACCOUNTS")
    if partner_accounts:
        return partner_accounts.split(',')
    return []

from dotenv import load_dotenv
import os

load_dotenv()

def get_partner_accounts():
    try:
        partner_accounts = os.getenv("PARTNER_ACCOUNTS")
        if partner_accounts:
            accounts = partner_accounts.split(',')
            print(f"[Success] Partner accounts retrieved.")
            return accounts
        print("[Info] No partner accounts set.")
        return []
    except Exception as e:
        print(f"[Error] Error getting partner accounts: {e}")
        return []

def get_ignore_payment_accounts():
    try:
        ignore_payment_accounts = os.getenv("IGNORE_PAYMENT_ACCOUNTS")
        if ignore_payment_accounts:
            accounts = ignore_payment_accounts.split(',')
            print(f"[Success] Ignore payment accounts retrieved.")
            return accounts
        print("[Info] No ignore payment accounts set.")
        return []
    except Exception as e:
        print(f"[Error] Error getting ignore payment accounts: {e}")
        return []

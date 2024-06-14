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

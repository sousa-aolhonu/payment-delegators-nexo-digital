from beem import Hive
from beem.account import Account
from hiveengine.wallet import Wallet as HiveEngineWallet
from dotenv import load_dotenv
import os
import hashlib
from Crypto.Hash import RIPEMD160

load_dotenv()

def new_hash(name, data=b""):
    if name == "ripemd160":
        return RIPEMD160.new(data)
    else:
        return hashlib.new(name, data)

hashlib.new = new_hash

def configure_hive():
    try:
        stm = Hive(node="https://api.hive.blog", keys=[os.getenv("HIVE_ENGINE_ACTIVE_PRIVATE_KEY"), os.getenv("HIVE_ENGINE_POSTING_PRIVATE_KEY")])
        account = Account(os.getenv("PAYMENT_ACCOUNT"), blockchain_instance=stm)
        print("[Success] Hive configured successfully.")
        return stm, account
    except Exception as e:
        print(f"[Error] Error configuring Hive: {e}")
        return None, None

def configure_hive_engine_wallet(account, stm):
    try:
        wallet = HiveEngineWallet(account.name, steem_instance=stm)
        print("[Success] Hive Engine Wallet configured successfully.")
        return wallet
    except Exception as e:
        print(f"[Error] Error configuring Hive Engine Wallet: {e}")
        return None

def check_balance(wallet):
    try:
        balances = wallet.get_balances()
        nexo_balance = next((item["balance"] for item in balances if item["symbol"] == "NEXO"), 0.0)
        print(f"[Success] NEXO balance retrieved: {nexo_balance}")
        return float(nexo_balance)
    except Exception as e:
        print(f"[Error] Error checking NEXO balance: {e}")
        return 0.0

def process_payments(df):
    try:
        payments_enabled = os.getenv("ACTIVATE_PAYMENTS", "False") == "True"
        if not payments_enabled:
            print("[Info] Payments are deactivated. Only spreadsheets were generated.")
            return

        stm, payment_account = configure_hive()
        if not stm or not payment_account:
            print("[Error] Failed to configure Hive.")
            return

        wallet = configure_hive_engine_wallet(payment_account, stm)
        if not wallet:
            print("[Error] Failed to configure Hive Engine Wallet.")
            return

        nexo_balance = check_balance(wallet)

        token_name = os.getenv('TOKEN_NAME', 'NEXO')
        receiver_account = os.getenv('RECEIVER_ACCOUNT')
        partner_accounts = os.getenv('PARTNER_ACCOUNTS', '').split(',')

        for index, row in df.iterrows():
            try:
                delegator = row["Account"]
                payment_column_name = f"{token_name} Payment"
                payment_amount = float(row.get(payment_column_name, 0))

                if delegator not in [receiver_account, "Partner Accounts", "Total", "Earnings for the period", "APR"] + partner_accounts and payment_amount > 0:
                    if payment_amount <= nexo_balance:
                        wallet.transfer(delegator, str(f"{payment_amount:.3f}"), token_name, "Delegation payment")
                        nexo_balance -= payment_amount
                        print(f"[Success] Payment of {payment_amount} {token_name} to {delegator} completed successfully.")
                    else:
                        print(f"[Error] Insufficient balance to pay {payment_amount} {token_name} to {delegator}.")
            except Exception as e:
                print(f"[Error] Error making payment to {delegator}: {e}")

        print(f"[Success] Updated {token_name} balance after payments: {nexo_balance}")
    except Exception as e:
        print(f"[Error] Error in payment process: {e}")

import time
from beem import Hive
from beem.account import Account
from hiveengine.wallet import Wallet as HiveEngineWallet
from dotenv import load_dotenv
import os
import hashlib
from Crypto.Hash import RIPEMD160
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

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
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Hive configured successfully.")
        return stm, account
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error configuring Hive: {e}")
        return None, None

def configure_hive_engine_wallet(account, stm):
    try:
        wallet = HiveEngineWallet(account.name, steem_instance=stm)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Hive Engine Wallet configured successfully.")
        return wallet
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error configuring Hive Engine Wallet: {e}")
        return None

def check_balance(wallet):
    try:
        balances = wallet.get_balances()
        nexo_balance = next((item["balance"] for item in balances if item["symbol"] == "NEXO"), 0.0)
        nexo_balance = float(nexo_balance)  # Garantir que seja float antes de arredondar
        nexo_balance = round(nexo_balance, 3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} NEXO balance retrieved: {Fore.YELLOW}{nexo_balance}{Style.RESET_ALL}")
        return nexo_balance
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error checking NEXO balance: {e}")
        return 0.0

def process_payments(df):
    try:
        payments_enabled = os.getenv("ACTIVATE_PAYMENTS", "False") == "True"
        if not payments_enabled:
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Payments are deactivated. Only spreadsheets were generated.")
            return

        stm, payment_account = configure_hive()
        if not stm or not payment_account:
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Failed to configure Hive.")
            return

        wallet = configure_hive_engine_wallet(payment_account, stm)
        if not wallet:
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Failed to configure Hive Engine Wallet.")
            return

        token_name = os.getenv('TOKEN_NAME', 'NEXO')
        receiver_account = os.getenv('RECEIVER_ACCOUNT')
        partner_accounts = os.getenv('PARTNER_ACCOUNTS', '').split(',')
        ignore_payment_accounts = os.getenv('IGNORE_PAYMENT_ACCOUNTS', '').split(',')

        payments_made = False

        for index, row in df.iterrows():
            try:
                delegator = row["Account"]
                payment_column_name = f"{token_name} Payment"
                payment_amount = float(row.get(payment_column_name, 0))

                if delegator not in [receiver_account, "Partner Accounts", "Total", "Earnings for the period", "APR"] + partner_accounts and payment_amount > 0:
                    if delegator not in ignore_payment_accounts:
                        # Pause for 10 seconds to ensure transaction is reflected on the blockchain
                        time.sleep(10)
                        current_balance = check_balance(wallet)
                        if payment_amount <= current_balance:
                            wallet.transfer(delegator, str(f"{payment_amount:.3f}"), token_name, "Delegation payment")
                            payments_made = True
                            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Payment of {Fore.YELLOW}{payment_amount}{Style.RESET_ALL} {Fore.YELLOW}{token_name}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL} completed successfully.")
                        else:
                            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Insufficient balance to pay {Fore.YELLOW}{payment_amount}{Style.RESET_ALL} {Fore.YELLOW}{token_name}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL}.")
            except Exception as e:
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error making payment to {Fore.BLUE}{delegator}{Style.RESET_ALL}: {e}")

        if not payments_made:
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No payments were made because there were no eligible delegators or sufficient balances.")
        
        final_balance = check_balance(wallet)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Updated {Fore.YELLOW}{token_name}{Style.RESET_ALL} balance after payments: {Fore.YELLOW}{final_balance}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error in payment process: {e}")

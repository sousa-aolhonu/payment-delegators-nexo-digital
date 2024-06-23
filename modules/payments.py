import time
from beem import Hive
from beem.account import Account
from hiveengine.wallet import Wallet as HiveEngineWallet
from dotenv import load_dotenv
import os
import requests
import logging
from colorama import Fore, Style, init
from modules.process_payment import process_payment_for_delegator
from modules.wallet_utils import check_balance
from modules.memo_utils import generate_unique_hash, format_memo, get_current_date

init(autoreset=True)

load_dotenv()

def configure_hive():
    try:
        logging.info("Configuring Hive...")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Configuring Hive...")
        stm = Hive(node="https://api.hive.blog", keys=[os.getenv("HIVE_ENGINE_ACTIVE_PRIVATE_KEY"), os.getenv("HIVE_ENGINE_POSTING_PRIVATE_KEY")])
        account = Account(os.getenv("PAYMENT_ACCOUNT"), blockchain_instance=stm)
        logging.info("Hive configured successfully.")
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Hive configured successfully.")
        return stm, account
    except Exception as e:
        logging.error(f"Error configuring Hive: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error configuring Hive: {e}")
        return None, None

def configure_hive_engine_wallet(account, stm):
    try:
        logging.info("Configuring Hive Engine Wallet...")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Configuring Hive Engine Wallet...")
        wallet = HiveEngineWallet(account.name, steem_instance=stm)
        logging.info("Hive Engine Wallet configured successfully.")
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Hive Engine Wallet configured successfully.")
        return wallet
    except Exception as e:
        logging.error(f"Error configuring Hive Engine Wallet: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error configuring Hive Engine Wallet: {e}")
        return None

def memo_exists(payment_account, memo, token_name):
    try:
        logging.info(f"Checking for existing memo: {memo}")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Checking for existing memo: {memo}")
        url = f"https://history.hive-engine.com/accountHistory?account={payment_account}&limit=100&symbol={token_name}"
        response = requests.get(url)
        response.raise_for_status()
        transactions = response.json()
        for transaction in transactions:
            if transaction.get('memo') == memo:
                logging.warning(f"Memo already exists in transaction history: {memo}")
                print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} Memo already exists in transaction history: {memo}")
                return True
        return False
    except Exception as e:
        logging.error(f"Error checking for existing memo: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error checking for existing memo: {e}")
        return False

def process_payments(df):
    try:
        payments_enabled = os.getenv("ACTIVATE_PAYMENTS", "False") == "True"
        if not payments_enabled:
            logging.info("Payments are deactivated. Only spreadsheets will be generated.")
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Payments are deactivated. Only spreadsheets will be generated.")
            return

        logging.info("Configuring Hive and Wallet...")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Configuring Hive and Wallet...")
        stm, payment_account = configure_hive()
        if not stm or not payment_account:
            raise Exception("Failed to configure Hive")

        wallet = configure_hive_engine_wallet(payment_account, stm)
        if not wallet:
            raise Exception("Failed to configure Hive Engine Wallet")

        token_name = os.getenv('TOKEN_NAME', 'NEXO')
        receiver_account = os.getenv('RECEIVER_ACCOUNT')
        partner_accounts = os.getenv('PARTNER_ACCOUNTS', '').split(',')
        ignore_payment_accounts = os.getenv('IGNORE_PAYMENT_ACCOUNTS', '').split(',')

        payments_made = False
        df["TxID"] = ""
        df["Unique Hash"] = ""

        for index, row in df.iterrows():
            try:
                delegator = row["Account"]
                payment_column_name = f"{token_name} Payment"
                payment_amount = float(row.get(payment_column_name, 0))

                if delegator not in [receiver_account, "Partner Accounts", "Total", "Earnings for the period", "APR"] + partner_accounts and payment_amount > 0:
                    if delegator not in ignore_payment_accounts:
                        current_date = get_current_date()
                        unique_hash = generate_unique_hash(delegator, payment_amount, current_date)
                        memo = format_memo(delegator, payment_amount, current_date, unique_hash)
                        if not memo_exists(payment_account.name, memo, token_name):
                            logging.info(f"Processing reward for {delegator}...")
                            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Processing reward for {Fore.BLUE}{delegator}{Style.RESET_ALL}...")
                            if process_payment_for_delegator(wallet, payment_account, token_name, delegator, payment_amount, df, index):
                                payments_made = True
                            logging.info(f"Reward processed for {delegator}.")
                            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Reward processed for {Fore.BLUE}{delegator}{Style.RESET_ALL}.")
                        else:
                            logging.warning(f"Reward already processed for {delegator}. Skipping reward.")
                            print(f"{Fore.YELLOW}[Warning]{Style.RESET_ALL} Reward already processed for {Fore.BLUE}{delegator}{Style.RESET_ALL}. Skipping reward.")
            except Exception as e:
                logging.error(f"Error making reward to {delegator}: {e}")
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error making reward to {Fore.BLUE}{delegator}{Style.RESET_ALL}: {e}")

        if not payments_made:
            logging.info("No rewards were made because there were no eligible delegators or sufficient balances.")
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No rewards were made because there were no eligible delegators or sufficient balances.")
        
        final_balance = check_balance(wallet)
        logging.info(f"Updated {token_name} balance after rewards: {final_balance}")
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Updated {Fore.YELLOW}{token_name}{Style.RESET_ALL} balance after rewards: {Fore.YELLOW}{final_balance}")
    except Exception as e:
        logging.error(f"Error in reward process: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error in reward process: {e}")

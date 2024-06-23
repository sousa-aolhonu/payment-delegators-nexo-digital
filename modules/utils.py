import os
import pandas as pd
import logging
from colorama import Fore, Style, init
from modules.process_payment import process_payment_for_delegator
from modules.wallet_utils import configure_hive, configure_hive_engine_wallet

init(autoreset=True)

def get_latest_file(directory, prefix):
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Getting the latest file in directory {Fore.BLUE}{directory}{Style.RESET_ALL} with prefix {Fore.BLUE}{prefix}{Style.RESET_ALL}...")
        logging.info(f"Getting the latest file in directory {directory} with prefix {prefix}...")
        files = [f for f in os.listdir(directory) if f.startswith(prefix)]
        if not files:
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No files found.")
            logging.info("No files found.")
            return None
        files.sort(reverse=True)
        latest_file = os.path.join(directory, files[0])
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Latest file found: {Fore.BLUE}{latest_file}{Style.RESET_ALL}")
        logging.info(f"Latest file found: {latest_file}")
        return latest_file
    except Exception as e:
        logging.error(f"Error getting latest file: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting latest file: {e}")
        return None

def get_previous_own_hp(latest_file, receiver_account):
    try:
        if latest_file:
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Reading latest file {Fore.BLUE}{latest_file}{Style.RESET_ALL} to get previous own HP for {Fore.BLUE}{receiver_account}{Style.RESET_ALL}...")
            logging.info(f"Reading latest file {latest_file} to get previous own HP for {receiver_account}...")
            df = pd.read_excel(latest_file)
            previous_own_hp = df.loc[df['Account'] == receiver_account, 'Delegated HP'].values[0]
            previous_own_hp = float(str(previous_own_hp).replace(" HP", ""))
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Previous own HP retrieved: {Fore.YELLOW}{previous_own_hp}{Style.RESET_ALL}")
            logging.info(f"Previous own HP retrieved: {previous_own_hp}")
            return previous_own_hp
    except Exception as e:
        logging.error(f"Error getting previous own HP: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting previous own HP: {e}")
    return 0

def process_failed_payments():
    try:
        logging.info("Processing failed payments from the previous run.")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Processing failed payments from the previous run.")
        latest_file = get_latest_file('data', 'pd_')
        if not latest_file:
            logging.info("No previous file found. Skipping failed payments processing.")
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No previous file found. Skipping failed payments processing.")
            return

        df = pd.read_excel(latest_file)
        failed_payments = df[df['TxID'].isin(['Failed', 'Error'])]
        
        if failed_payments.empty:
            logging.info("No failed payments found in the previous file.")
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No failed payments found in the previous file.")
            return

        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Found {len(failed_payments)} failed payments. Reprocessing...")
        logging.info(f"Found {len(failed_payments)} failed payments. Reprocessing...")

        stm, payment_account = configure_hive()
        if not stm or not payment_account:
            raise Exception("Failed to configure Hive")

        wallet = configure_hive_engine_wallet(payment_account, stm)
        if not wallet:
            raise Exception("Failed to configure Hive Engine Wallet")

        token_name = os.getenv('TOKEN_NAME', 'NEXO')

        for index, row in failed_payments.iterrows():
            delegator = row['Account']
            payment_amount = float(row[f'{token_name} Payment'].replace(f' {token_name}', ''))
            original_date = row['Date'] if 'Date' in row else None
            process_payment_for_delegator(wallet, payment_account, token_name, delegator, payment_amount, df, index, original_date)
        
        df.to_excel(latest_file, index=False)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Reprocessed failed payments and updated the file: {Fore.BLUE}{latest_file}{Style.RESET_ALL}")
        logging.info(f"Reprocessed failed payments and updated the file: {latest_file}")
    except Exception as e:
        logging.error(f"Error processing failed payments: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error processing failed payments: {e}")

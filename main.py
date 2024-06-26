import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd
import time
from colorama import Fore, Style, init
from tabulate import tabulate
from modules.fetch_delegators import fetch_delegators
from modules.account_info import get_account_info, vests_to_hp
from modules.partners_info import get_partner_accounts, get_ignore_payment_accounts
from modules.utils import get_latest_file, get_previous_own_hp
from modules.save_to_xlsx import save_delegators_to_xlsx
from modules.payments import process_payments
from modules.calculations import calculate_additional_columns
from modules.logger import setup_logging
from modules.telegram_utils import send_telegram_file
from modules.discord_utils import send_discord_file
from modules.config import check_env_variables

init(autoreset=True)

def get_seconds_until_next_run(run_time):
    now = datetime.now()
    run_hour, run_minute = map(int, run_time.split(':'))
    next_run = now.replace(hour=run_hour, minute=run_minute, second=0, microsecond=0)

    if now >= next_run:
        next_run += timedelta(days=1)

    wait_time = (next_run - now).total_seconds()
    return wait_time

def get_own_hp(receiver_account):
    try:
        logging.debug(f"Starting to fetch own HP for {receiver_account}.")
        own_hp = get_account_info(receiver_account)
        logging.info(f"Own HP for {receiver_account} is {own_hp}")
        return own_hp
    except Exception as e:
        logging.error(f"Error fetching own HP for {receiver_account}: {e}")
        raise

def fetch_delegators_info(receiver_account):
    try:
        logging.info(f"Fetching delegators info for {receiver_account}...")
        
        delegators_list = fetch_delegators()
        logging.debug(f"Delegators list: {delegators_list}")

        partner_accounts = get_partner_accounts()
        logging.debug(f"Partner accounts: {partner_accounts}")

        ignore_payment_accounts = get_ignore_payment_accounts()
        logging.debug(f"Ignore payment accounts: {ignore_payment_accounts}")

        logging.info(f"Delegators info fetched successfully for {receiver_account}.")
        return delegators_list, partner_accounts, ignore_payment_accounts
    except Exception as e:
        logging.error(f"Error fetching delegators info for {receiver_account}: {e}")
        raise

def calculate_earnings(own_hp, receiver_account):
    try:
        logging.info(f"Calculating earnings for {receiver_account}...")
        
        latest_file = get_latest_file('data', 'pd_')
        logging.debug(f"Latest file found: {latest_file}")

        previous_own_hp = round(get_previous_own_hp(latest_file, receiver_account), 3)
        logging.debug(f"Previous own HP: {previous_own_hp}")

        earnings = round(own_hp - previous_own_hp, 3)
        logging.info(f"Earnings calculated: {earnings}")

        return earnings
    except Exception as e:
        logging.error(f"Error calculating earnings for {receiver_account}: {e}")
        raise

def process_delegators(delegators_list, partner_accounts):
    try:
        logging.info("Processing delegators list...")
        partner_hp = 0
        delegators = []
        for item in delegators_list:
            try:
                delegator = item['delegator']
                vesting_shares = float(item['vesting_shares'])
                delegated_hp = round(vests_to_hp(vesting_shares, delegator), 3)
                if delegator in partner_accounts:
                    partner_hp += delegated_hp
                else:
                    delegators.append({
                        "Account": delegator,
                        "Delegated HP": delegated_hp
                    })
                logging.debug(f"Processed delegator {delegator}: {delegated_hp} HP")
            except Exception as e:
                logging.error(f"Error processing delegator {item}: {e}")
        partner_hp = round(partner_hp, 3)
        logging.info(f"Delegators processed successfully. Partner HP: {partner_hp}")
        return delegators, partner_hp
    except Exception as e:
        logging.error(f"Error processing delegators: {e}")
        raise

def insert_accounts_into_df(delegators, receiver_account, receiver_hp, partner_hp):
    try:
        logging.info("Inserting accounts into DataFrame...")
        delegators.insert(0, {"Account": receiver_account, "Delegated HP": receiver_hp})
        delegators.insert(1, {"Account": "Partner Accounts", "Delegated HP": partner_hp})
        logging.debug(f"Receiver account and partner accounts inserted: {delegators[:2]}")
        logging.info("Accounts inserted into DataFrame successfully.")
        return delegators
    except Exception as e:
        logging.error(f"Error inserting accounts into DataFrame: {e}")
        raise

def main():
    try:
        load_dotenv()

        auto_run = os.getenv("AUTO_RUN", "False") == "True"
        run_time = os.getenv("RUN_TIME", "23:00")

        while True:
            now = datetime.now()
            timestamp = now.strftime("pd_%m-%d-%Y_%H-%M-%S")

            setup_logging(timestamp)
            check_env_variables()

            receiver_account = os.getenv("RECEIVER_ACCOUNT")
            own_hp = round(get_own_hp(receiver_account), 3)

            earnings = calculate_earnings(own_hp, receiver_account)

            delegators_list, partner_accounts, ignore_payment_accounts = fetch_delegators_info(receiver_account)

            delegators, partner_hp = process_delegators(delegators_list, partner_accounts)

            delegators = insert_accounts_into_df(delegators, receiver_account, own_hp, partner_hp)

            logging.info("Calculating additional columns...")
            df = calculate_additional_columns(delegators, earnings)
            df["Unique Hash"] = ""
            logging.info("Additional columns calculated successfully.")

            logging.info("DataFrame before rewards:")
            df_display = df.copy()
            df_display["Delegated HP"] = df_display.apply(
                lambda x: f"{x['Delegated HP']} HP" if x["Account"] != "APR" else x["Delegated HP"],
                axis=1
            )
            df_display["HIVE Deduction"] = df_display["HIVE Deduction"].apply(lambda x: f"{x} HIVE" if x != "" else x)
            token_name = os.getenv("TOKEN_NAME", "NEXO")
            df_display[f"{token_name} Payment"] = df_display[f"{token_name} Payment"].apply(lambda x: f"{x} {token_name}" if x != "" else x)
            df_display["Percentage"] = df_display["Percentage"].apply(lambda x: f"{x}%" if pd.notnull(x) and x != "" and not str(x).endswith('%') else x)
            print(tabulate(df_display, headers='keys', tablefmt='psql'))
            logging.debug(f"\n{tabulate(df_display, headers='keys', tablefmt='psql')}")

            logging.info("Processing rewards...")
            payments_enabled = os.getenv("ACTIVATE_PAYMENTS", "False") == "True"
            if payments_enabled:
                process_payments(df)
            else:
                print(tabulate(df_display, headers='keys', tablefmt='psql'))
                logging.info("Payments are deactivated. Only spreadsheets will be generated.")

            logging.info("Saving delegators list to XLSX...")
            save_delegators_to_xlsx(df, earnings)

            logging.info("All tasks completed successfully.")

            log_file_path = f"data/log/log_{timestamp}.txt"
            telegram_success = send_telegram_file(log_file_path, "Log file for the latest execution")
            if telegram_success:
                logging.info("Log file sent successfully to Telegram.")
            else:
                logging.error("Failed to send log file to Telegram.")

            latest_xlsx_file = get_latest_file('data', 'pd_')
            discord_success = send_discord_file(latest_xlsx_file, "Spreadsheet for the latest execution")
            if discord_success:
                logging.info("Spreadsheet file sent successfully to Discord.")
            else:
                logging.error("Failed to send spreadsheet file to Discord.")

            if auto_run:
                wait_time = get_seconds_until_next_run(run_time)
                logging.info(f"Waiting for {wait_time} seconds until next execution at {run_time}...")
                time.sleep(wait_time)
            else:
                break

    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()

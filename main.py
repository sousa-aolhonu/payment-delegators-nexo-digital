import os
from dotenv import load_dotenv
import pandas as pd
from colorama import Fore, Style, init
from modules.fetch_delegators import fetch_delegators
from modules.account_info import get_account_info, vests_to_hp
from modules.partners_info import get_partner_accounts, get_ignore_payment_accounts
from modules.utils import get_latest_file, get_previous_own_hp
from modules.save_to_xlsx import save_delegators_to_xlsx
from modules.payments import process_payments
from modules.calculations import calculate_additional_columns
from tabulate import tabulate

init(autoreset=True)

load_dotenv()

def check_env_variables():
    """
    Checks if all required environment variables are set.

    Raises:
        EnvironmentError: If any required environment variable is not set.
    """
    required_vars = [
        "RECEIVER_ACCOUNT", "PAYMENT_ACCOUNT", "HIVE_ENGINE_ACTIVE_PRIVATE_KEY", 
        "HIVE_ENGINE_POSTING_PRIVATE_KEY", "TOKEN_NAME", "TOKEN_FIXED_PRICE", 
        "HIVE_DEDUCTION_MULTIPLIER", "ACTIVATE_PAYMENTS"
    ]
    for var in required_vars:
        if not os.getenv(var):
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Environment variable {Fore.BLUE}{var}{Style.RESET_ALL} is not set")
            raise EnvironmentError(f"Environment variable {var} is not set")
        else:
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Environment variable {Fore.BLUE}{var}{Style.RESET_ALL} is set: {Fore.YELLOW}{os.getenv(var)}")

def get_own_hp(receiver_account):
    """
    Fetches the own HP (Hive Power) for the receiver account.

    Args:
        receiver_account (str): The name of the receiver account.

    Returns:
        float: The own HP of the receiver account.

    Raises:
        Exception: If there is an error fetching the account information.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching own HP for {Fore.BLUE}{receiver_account}{Style.RESET_ALL}...")
        own_hp = get_account_info(receiver_account)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Own HP for {Fore.BLUE}{receiver_account}{Style.RESET_ALL} is {Fore.YELLOW}{own_hp}")
        return own_hp
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error fetching own HP for {Fore.BLUE}{receiver_account}{Style.RESET_ALL}: {e}")
        raise

def fetch_delegators_info(receiver_account):
    """
    Fetches the delegators list, partner accounts, and ignore payment accounts for the receiver account.

    Args:
        receiver_account (str): The name of the receiver account.

    Returns:
        tuple: A tuple containing the delegators list, partner accounts, and ignore payment accounts.

    Raises:
        Exception: If there is an error fetching the delegators info.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching delegators list for {Fore.BLUE}{receiver_account}{Style.RESET_ALL}...")
        delegators_list = fetch_delegators()
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Delegators list fetched successfully.")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching partner accounts...")
        partner_accounts = get_partner_accounts()
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Partner accounts fetched successfully.")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching ignore payment accounts...")
        ignore_payment_accounts = get_ignore_payment_accounts()
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Ignore payment accounts fetched successfully.")
        return delegators_list, partner_accounts, ignore_payment_accounts
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error fetching delegators info: {e}")
        raise

def calculate_earnings(own_hp, receiver_account):
    """
    Calculates the earnings for the period.

    Args:
        own_hp (float): The own HP of the receiver account.
        receiver_account (str): The name of the receiver account.

    Returns:
        float: The earnings for the period.

    Raises:
        Exception: If there is an error calculating the earnings.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching latest file for {Fore.BLUE}{receiver_account}{Style.RESET_ALL}...")
        latest_file = get_latest_file('data', 'pd_')
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Latest file found: {Fore.YELLOW}{latest_file}")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching previous own HP from latest file...")
        previous_own_hp = round(get_previous_own_hp(latest_file, receiver_account), 3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Previous own HP: {Fore.YELLOW}{previous_own_hp}")
        earnings = round(own_hp - previous_own_hp, 3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Earnings calculated: {Fore.YELLOW}{earnings}")
        return earnings
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error calculating earnings: {e}")
        raise

def process_delegators(delegators_list, partner_accounts):
    """
    Processes the delegators list to calculate delegated HP for each delegator.

    Args:
        delegators_list (list): The list of delegators.
        partner_accounts (list): The list of partner accounts.

    Returns:
        tuple: A tuple containing the processed delegators list and the total HP of partner accounts.

    Raises:
        Exception: If there is an error processing the delegators.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Processing delegators list...")
        partner_hp = 0
        delegators = []
        for item in delegators_list:
            try:
                delegator = item['delegator']
                vesting_shares = float(item['vesting_shares'].replace(' VESTS', ''))
                delegated_hp = round(vests_to_hp(vesting_shares, delegator), 3)
                if delegator in partner_accounts:
                    partner_hp += delegated_hp
                else:
                    delegators.append({
                        "Account": delegator,
                        "Delegated HP": delegated_hp
                    })
                print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Processed delegator {Fore.BLUE}{delegator}{Style.RESET_ALL}: {Fore.YELLOW}{delegated_hp} HP")
            except Exception as e:
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error processing delegator {Fore.BLUE}{item}{Style.RESET_ALL}: {e}")
        partner_hp = round(partner_hp, 3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Delegators processed successfully. Partner HP: {Fore.YELLOW}{partner_hp}")
        return delegators, partner_hp
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error processing delegators: {e}")
        raise

def insert_accounts_into_df(delegators, receiver_account, receiver_hp, partner_hp):
    """
    Inserts the receiver account and partner accounts into the DataFrame.

    Args:
        delegators (list): The list of delegators.
        receiver_account (str): The name of the receiver account.
        receiver_hp (float): The own HP of the receiver account.
        partner_hp (float): The total HP of the partner accounts.

    Returns:
        list: The updated list of delegators with the receiver and partner accounts inserted.

    Raises:
        Exception: If there is an error inserting the accounts into the DataFrame.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Inserting accounts into DataFrame...")
        delegators.insert(0, {"Account": receiver_account, "Delegated HP": receiver_hp})
        delegators.insert(1, {"Account": "Partner Accounts", "Delegated HP": partner_hp})
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Accounts inserted into DataFrame successfully.")
        return delegators
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error inserting accounts into DataFrame: {e}")
        raise

def main():
    """
    Main function to execute the program.

    Checks environment variables, fetches account information, calculates earnings,
    processes delegators, calculates additional columns, processes payments,
    and saves the delegators list to an XLSX file.
    """
    try:
        check_env_variables()

        receiver_account = os.getenv("RECEIVER_ACCOUNT")
        own_hp = round(get_own_hp(receiver_account), 3)

        earnings = calculate_earnings(own_hp, receiver_account)

        delegators_list, partner_accounts, ignore_payment_accounts = fetch_delegators_info(receiver_account)

        delegators, partner_hp = process_delegators(delegators_list, partner_accounts)

        delegators = insert_accounts_into_df(delegators, receiver_account, own_hp, partner_hp)

        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Calculating additional columns...")
        df = calculate_additional_columns(delegators, earnings)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Additional columns calculated successfully.")

        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} DataFrame before payments:")
        print(tabulate(df, headers='keys', tablefmt='psql'))

        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Processing payments...")
        process_payments(df)

        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Saving delegators list to XLSX...")
        save_delegators_to_xlsx(df, earnings)

        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} All tasks completed successfully.")
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error in main execution: {e}")

if __name__ == "__main__":
    main()

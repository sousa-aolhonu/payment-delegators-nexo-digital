import pandas as pd
import os
import logging
from dotenv import load_dotenv
from colorama import Fore, Style, init

init(autoreset=True)

load_dotenv()

def calculate_additional_columns(delegators, earnings):
    """
    Calculates additional columns for the DataFrame of delegators.

    Args:
        delegators (list of dict): List of delegators with their account names and delegated HP.
        earnings (float): The earnings for the period.

    Returns:
        pd.DataFrame: DataFrame with additional columns calculated, or an empty DataFrame if an error occurs.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Calculating additional columns...")
        df = pd.DataFrame(delegators)
        df["Delegated HP"] = pd.to_numeric(df["Delegated HP"], errors='coerce')

        total_hp = df["Delegated HP"].sum().round(3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Total Delegated HP: {Fore.YELLOW}{total_hp}")

        df["Percentage"] = (df["Delegated HP"] / total_hp * 100).round(3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Percentage of each delegator's HP calculated.")

        hive_deduction_multiplier = float(os.getenv("HIVE_DEDUCTION_MULTIPLIER", 2))
        df["HIVE Deduction"] = (df["Percentage"] * earnings * hive_deduction_multiplier / 100).round(3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} HIVE Deduction calculated with multiplier {Fore.YELLOW}{hive_deduction_multiplier}")

        token_name = os.getenv("TOKEN_NAME", "NEXO")
        token_fixed_price = float(os.getenv("TOKEN_FIXED_PRICE", 0.1))
        df[f"{token_name} Payment"] = ((df["HIVE Deduction"] * token_fixed_price) * 100).round(3)
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} {token_name} Payment calculated with fixed price {Fore.YELLOW}{token_fixed_price}")

        df["TxID"] = "Pending"
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} TxID column initialized with 'Pending' status.")

        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Additional columns calculated successfully.")
        return df
    except Exception as e:
        logging.error(f"Error calculating additional columns: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error calculating additional columns: {e}")
        return pd.DataFrame()

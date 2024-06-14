import pandas as pd
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

load_dotenv()

def calculate_additional_columns(delegators, earnings):
    try:
        df = pd.DataFrame(delegators)
        df["Delegated HP"] = pd.to_numeric(df["Delegated HP"], errors='coerce')

        total_hp = df["Delegated HP"].sum().round(3)
        df["Percentage"] = (df["Delegated HP"] / total_hp * 100).round(3)

        hive_deduction_multiplier = float(os.getenv("HIVE_DEDUCTION_MULTIPLIER", 2))
        df["HIVE Deduction"] = (df["Percentage"] * earnings * hive_deduction_multiplier / 100).round(3)

        token_name = os.getenv("TOKEN_NAME", "NEXO")
        token_fixed_price = float(os.getenv("TOKEN_FIXED_PRICE", 0.1))
        df[f"{token_name} Payment"] = ((df["HIVE Deduction"] * token_fixed_price) * 100).round(3)

        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Calculated additional columns.")
        return df
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error calculating additional columns: {e}")
        return pd.DataFrame()

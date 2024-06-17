import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

load_dotenv()

def save_delegators_to_xlsx(df, earnings):
    """
    Saves the delegators list to an XLSX file.

    Args:
        df (pd.DataFrame): The DataFrame containing the delegators and their details.
        earnings (float): The earnings for the period.

    Returns:
        None
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Preparing to save delegators list to XLSX...")
        now = datetime.now()
        timestamp = now.strftime("pd_%m-%d-%Y_%H-%M-%S")
        filename = f"data/{timestamp}.xlsx"
        
        total_hp = df["Delegated HP"].sum().round(3)
        total_hive_deduction = df["HIVE Deduction"].sum().round(3)
        token_name = os.getenv("TOKEN_NAME", "NEXO")
        total_token_payment = df[f"{token_name} Payment"].sum().round(3)

        current_year = now.year
        is_leap_year = (current_year % 4 == 0 and current_year % 100 != 0) or (current_year % 400 == 0)
        days_in_year = 366 if is_leap_year else 365

        apr = (((total_hive_deduction * days_in_year) / total_hp) * 100).round(3)

        total_row = pd.DataFrame([{
            "Account": "Total",
            "Delegated HP": total_hp,
            "Percentage": 100.000,
            "HIVE Deduction": total_hive_deduction,
            f"{token_name} Payment": total_token_payment,
            "TxID": ""
        }])

        df = pd.concat([df, total_row], ignore_index=True)

        earnings_row = pd.DataFrame([{
            "Account": "Earnings for the period",
            "Delegated HP": round(earnings, 3),
            "Percentage": "",
            "HIVE Deduction": "",
            f"{token_name} Payment": "",
            "TxID": ""
        }])

        apr_row = pd.DataFrame([{
            "Account": "APR",
            "Delegated HP": apr,
            "Percentage": "",
            "HIVE Deduction": "",
            f"{token_name} Payment": "",
            "TxID": ""
        }])

        df = pd.concat([df, earnings_row, apr_row], ignore_index=True)

        # Add hyperlinks to the TxID column
        for i in range(len(df)):
            txid = df.at[i, "TxID"]
            if txid and txid not in ["Not found", "Failed", "Error", ""]:
                df.at[i, "TxID"] = f'=HYPERLINK("https://he.dtools.dev/tx/{txid}", "{txid}")'

        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Delegators')
            workbook  = writer.book
            worksheet = writer.sheets['Delegators']

            for i, txid in enumerate(df["TxID"]):
                if txid.startswith('=HYPERLINK'):
                    worksheet.write_formula(i + 1, df.columns.get_loc("TxID"), txid)

        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Delegators list successfully saved in '{Fore.YELLOW}{filename}{Style.RESET_ALL}'.")
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error saving delegators to XLSX: {e}")

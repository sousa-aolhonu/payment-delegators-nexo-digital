import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

load_dotenv()

def save_delegators_to_xlsx(df, earnings):
    try:
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

        # Save to XLSX with hyperlinks
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Delegators')
            workbook = writer.book
            worksheet = writer.sheets['Delegators']
            
            # Add hyperlinks to TxID column
            for row_num, value in enumerate(df['TxID'], start=1):
                if value and value != "":
                    url = f"https://he.dtools.dev/tx/{value}"
                    worksheet.write_url(f'F{row_num+1}', url, string=value)
        
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Delegators list successfully saved in '{Fore.YELLOW}{filename}{Style.RESET_ALL}'.")
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error saving delegators to XLSX: {e}")

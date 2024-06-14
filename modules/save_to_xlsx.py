import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

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
            f"{token_name} Payment": total_token_payment
        }])

        df = pd.concat([df, total_row], ignore_index=True)

        earnings_row = pd.DataFrame([{
            "Account": "Earnings for the period",
            "Delegated HP": round(earnings, 3),
            "Percentage": "",
            "HIVE Deduction": "",
            f"{token_name} Payment": ""
        }])

        apr_row = pd.DataFrame([{
            "Account": "APR",
            "Delegated HP": apr,
            "Percentage": "",
            "HIVE Deduction": "",
            f"{token_name} Payment": ""
        }])

        df = pd.concat([df, earnings_row, apr_row], ignore_index=True)

        df.to_excel(filename, index=False)
        print(f"[Success] Delegators list successfully saved in '{filename}'.")
    except Exception as e:
        print(f"[Error] Error saving delegators to XLSX: {e}")

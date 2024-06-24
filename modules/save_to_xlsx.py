import pandas as pd
from datetime import datetime
import os
import logging
from dotenv import load_dotenv
from colorama import Fore, Style, init

init(autoreset=True)

load_dotenv()

def save_delegators_to_xlsx(df, earnings):
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Preparing to save delegators list to XLSX...")
        now = datetime.now()
        timestamp = now.strftime("pd_%m-%d-%Y_%H-%M-%S")
        filename = f"data/{timestamp}.xlsx"
        
        total_hp = df["Delegated HP"].astype(float).sum().round(3)
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
            "Percentage": "100%",
            "HIVE Deduction": total_hive_deduction,
            f"{token_name} Payment": total_token_payment,
            "TxID": "",
            "Unique Hash": ""
        }])

        df = pd.concat([df, total_row], ignore_index=True)

        earnings_row = pd.DataFrame([{
            "Account": "Earnings for the period",
            "Delegated HP": earnings,
            "Percentage": "",
            "HIVE Deduction": "",
            f"{token_name} Payment": "",
            "TxID": "",
            "Unique Hash": ""
        }])

        apr_row = pd.DataFrame([{
            "Account": "APR",
            "Delegated HP": f"{apr}%",
            "Percentage": "",
            "HIVE Deduction": "",
            f"{token_name} Payment": "",
            "TxID": "",
            "Unique Hash": ""
        }])

        df = pd.concat([df, earnings_row, apr_row], ignore_index=True)

        receiver_account = os.getenv("RECEIVER_ACCOUNT")
        df_reordered = pd.concat([
            df[df["Account"] == receiver_account],
            df[df["Account"] == "Partner Accounts"],
            df[~df["Account"].isin([receiver_account, "Partner Accounts", "Total", "Earnings for the period", "APR"])].sort_values(by="Delegated HP", ascending=False),
            df[df["Account"].isin(["Total", "Earnings for the period", "APR"])]
        ], ignore_index=True)

        if "Memo" in df_reordered.columns:
            df_reordered = df_reordered.drop(columns=["Memo"])

        df_reordered_display = df_reordered.copy()
        df_reordered_display["Delegated HP"] = df_reordered_display.apply(
            lambda x: f"{x['Delegated HP']} HP" if x["Account"] != "APR" else x["Delegated HP"],
            axis=1
        )

        def add_hive_display(value):
            if value != "" and not str(value).endswith(" HIVE"):
                return f"{value} HIVE"
            return value

        df_reordered_display["HIVE Deduction"] = df_reordered_display["HIVE Deduction"].apply(add_hive_display)

        def format_percentage(x):
            if pd.notnull(x) and x != "" and not str(x).endswith('%'):
                return f"{x}%"
            return x

        df_reordered_display["Percentage"] = df_reordered_display["Percentage"].apply(format_percentage)

        def add_token_display(value):
            if value != "" and not str(value).endswith(f" {token_name}"):
                return f"{value} {token_name}"
            return value

        df_reordered_display[f"{token_name} Payment"] = df_reordered_display[f"{token_name} Payment"].apply(add_token_display)

        for i in range(len(df_reordered_display)):
            txid = df_reordered_display.at[i, "TxID"]
            if txid and txid not in ["Not found", "Failed", "Error", ""]:
                df_reordered_display.at[i, "TxID"] = f'=HYPERLINK("https://he.dtools.dev/tx/{txid}", "{txid}")'

        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df_reordered_display.to_excel(writer, index=False, sheet_name='Delegators')
            workbook  = writer.book
            worksheet = writer.sheets['Delegators']

            for i, txid in enumerate(df_reordered_display["TxID"]):
                if txid.startswith('=HYPERLINK'):
                    worksheet.write_formula(i + 1, df_reordered_display.columns.get_loc("TxID"), txid)

        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Delegators list successfully saved in '{Fore.YELLOW}{filename}{Style.RESET_ALL}'.")
    except Exception as e:
        logging.error(f"Error saving delegators to XLSX: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error saving delegators to XLSX: {e}")

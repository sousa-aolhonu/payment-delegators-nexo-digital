import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

init(autoreset=True)

load_dotenv()


def save_delegators_to_xlsx(df, earnings):
    try:
        print(
            f"{Fore.CYAN}[Info]{Style.RESET_ALL} Preparing to save delegators list to XLSX..."
        )
        now = datetime.now()
        timestamp = now.strftime("pd_%m-%d-%Y_%H-%M-%S")
        filename = f"data/{timestamp}.xlsx"

        total_hp = df["Delegated HP"].sum().round(3)
        total_hive_deduction = df["HIVE Deduction"].sum().round(3)
        token_name = os.getenv("TOKEN_NAME", "NEXO")
        total_token_payment = df[f"{token_name} Payment"].sum().round(3)

        current_year = now.year
        is_leap_year = (current_year % 4 == 0 and current_year % 100 != 0) or (
            current_year % 400 == 0
        )
        days_in_year = 366 if is_leap_year else 365

        apr = (((total_hive_deduction * days_in_year) / total_hp) * 100).round(3)

        total_row = pd.DataFrame(
            [
                {
                    "Account": "Total",
                    "Delegated HP": total_hp,
                    "Percentage": 100.000,
                    "HIVE Deduction": total_hive_deduction,
                    f"{token_name} Payment": total_token_payment,
                    "TxID": "",
                    "Unique Hash": "",
                }
            ]
        )

        df = pd.concat([df, total_row], ignore_index=True)

        earnings_row = pd.DataFrame(
            [
                {
                    "Account": "Earnings for the period",
                    "Delegated HP": round(earnings, 3),
                    "Percentage": "",
                    "HIVE Deduction": "",
                    f"{token_name} Payment": "",
                    "TxID": "",
                    "Unique Hash": "",
                }
            ]
        )

        apr_row = pd.DataFrame(
            [
                {
                    "Account": "APR",
                    "Delegated HP": apr,
                    "Percentage": "",
                    "HIVE Deduction": "",
                    f"{token_name} Payment": "",
                    "TxID": "",
                    "Unique Hash": "",
                }
            ]
        )

        df = pd.concat([df, earnings_row, apr_row], ignore_index=True)

        receiver_account = os.getenv("RECEIVER_ACCOUNT")
        df_reordered = pd.concat(
            [
                df[df["Account"] == receiver_account],
                df[df["Account"] == "Partner Accounts"],
                df[
                    ~df["Account"].isin(
                        [
                            receiver_account,
                            "Partner Accounts",
                            "Total",
                            "Earnings for the period",
                            "APR",
                        ]
                    )
                ].sort_values(by="Delegated HP", ascending=False),
                df[df["Account"].isin(["Total", "Earnings for the period", "APR"])],
            ],
            ignore_index=True,
        )

        if "Memo" in df_reordered.columns:
            df_reordered = df_reordered.drop(columns=["Memo"])

        for i in range(len(df_reordered)):
            txid = df_reordered.at[i, "TxID"]
            if txid and txid not in ["Not found", "Failed", "Error", ""]:
                df_reordered.at[i, "TxID"] = (
                    f'=HYPERLINK("https://he.dtools.dev/tx/{txid}", "{txid}")'
                )

        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            df_reordered.to_excel(writer, index=False, sheet_name="Delegators")
            workbook = writer.book
            worksheet = writer.sheets["Delegators"]

            for i, txid in enumerate(df_reordered["TxID"]):
                if txid.startswith("=HYPERLINK"):
                    worksheet.write_formula(
                        i + 1, df_reordered.columns.get_loc("TxID"), txid
                    )

        print(
            f"{Fore.GREEN}[Success]{Style.RESET_ALL} Delegators list successfully saved in '{Fore.YELLOW}{filename}{Style.RESET_ALL}'."
        )
    except Exception as e:
        print(
            f"{Fore.RED}[Error]{Style.RESET_ALL} Error saving delegators to XLSX: {e}"
        )

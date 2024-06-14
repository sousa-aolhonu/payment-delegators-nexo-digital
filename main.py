import os
from dotenv import load_dotenv
import pandas as pd
from modules.fetch_delegators import fetch_delegators
from modules.account_info import get_account_info, vests_to_hp
from modules.partners_info import get_partner_accounts
from modules.utils import get_latest_file, get_previous_own_hp
from modules.save_to_xlsx import save_delegators_to_xlsx
from modules.payments import process_payments
from modules.calculations import calculate_additional_columns

load_dotenv()

def get_own_hp(receiver_account):
    try:
        return get_account_info(receiver_account)
    except Exception as e:
        print(f"[Error] Error fetching own HP: {e}")
        return 0

def process_delegators(delegators_list, partner_accounts):
    partner_hp = 0
    delegators = []
    for item in delegators_list:
        try:
            delegator = item['delegator']
            vesting_shares = float(item['vesting_shares'].replace(' VESTS', ''))
            delegated_hp = round(vests_to_hp(vesting_shares), 3)
            if delegator in partner_accounts:
                partner_hp += delegated_hp
            else:
                delegators.append({
                    "Account": delegator,
                    "Delegated HP": delegated_hp
                })
        except Exception as e:
            print(f"[Error] Error processing delegator {item}: {e}")
    partner_hp = round(partner_hp, 3)
    return delegators, partner_hp

def main():
    try:
        receiver_account = os.getenv("RECEIVER_ACCOUNT")
        print(f"[Info] Fetching own HP for {receiver_account}...")
        own_hp = round(get_own_hp(receiver_account), 3)

        print(f"[Info] Fetching latest file...")
        latest_file = get_latest_file('data', 'pd_')
        previous_own_hp = round(get_previous_own_hp(latest_file, receiver_account), 3)

        earnings = round(own_hp - previous_own_hp, 3)

        print(f"[Info] Fetching delegators list...")
        delegators_list = fetch_delegators()
        partner_accounts = get_partner_accounts()

        delegators, partner_hp = process_delegators(delegators_list, partner_accounts)

        delegators.insert(0, {"Account": receiver_account, "Delegated HP": own_hp})
        delegators.insert(1, {"Account": "Partner Accounts", "Delegated HP": partner_hp})

        print(f"[Info] Calculating additional columns...")
        df = calculate_additional_columns(delegators, earnings)

        print(f"[Info] Saving delegators list to XLSX...")
        save_delegators_to_xlsx(df, earnings)

        print(f"[Info] Processing payments...")
        process_payments(df)

    except Exception as e:
        print(f"[Error] Error in main execution: {e}")

if __name__ == "__main__":
    main()

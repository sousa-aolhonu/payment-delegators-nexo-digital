import os
from dotenv import load_dotenv
from modules.fetch_delegators import fetch_delegators
from modules.account_info import get_account_info, vests_to_hp
from modules.partners_info import get_partner_accounts
from modules.save_to_csv import save_delegators_to_csv

# Load environment variables
load_dotenv()

def main():
    receiver_account = os.getenv("RECEIVER_ACCOUNT")
    own_hp = get_account_info(receiver_account)
    
    delegators_list = fetch_delegators()
    partner_accounts = get_partner_accounts()
    
    partner_hp = 0
    delegators = []
    for item in delegators_list:
        delegator = item['delegator']
        vesting_shares = float(item['vesting_shares'].replace(' VESTS', ''))
        delegated_hp = vests_to_hp(vesting_shares)
        if delegator in partner_accounts:
            partner_hp += delegated_hp
        else:
            delegators.append({
                "Account": delegator,
                "Delegated HP": delegated_hp
            })
    
    delegators.insert(0, {"Account": receiver_account, "Delegated HP": own_hp})
    delegators.insert(1, {"Account": "Partner Accounts", "Delegated HP": partner_hp})

    save_delegators_to_csv(delegators)

if __name__ == "__main__":
    main()

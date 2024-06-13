import os
from dotenv import load_dotenv
from modules.fetch_delegators import fetch_delegators
from modules.account_info import get_account_info, vests_to_hp
from modules.partners_info import get_partner_accounts
from modules.utils import get_latest_file, get_previous_own_hp
from modules.save_to_xlsx import save_delegators_to_xlsx  # Ensure correct import

# Load environment variables
load_dotenv()

def get_own_hp(receiver_account):
    """Fetch the HP of the receiver account."""
    return get_account_info(receiver_account)

def process_delegators(delegators_list, partner_accounts):
    """Process the list of delegators to separate partner accounts and calculate HP."""
    partner_hp = 0
    delegators = []
    for item in delegators_list:
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
    partner_hp = round(partner_hp, 3)
    return delegators, partner_hp

def main():
    receiver_account = os.getenv("RECEIVER_ACCOUNT")
    own_hp = round(get_own_hp(receiver_account), 3)
    
    latest_file = get_latest_file('data', 'pd_')
    previous_own_hp = round(get_previous_own_hp(latest_file, receiver_account), 3)
    
    earnings = round(own_hp - previous_own_hp, 3)
    
    delegators_list = fetch_delegators()
    partner_accounts = get_partner_accounts()
    
    delegators, partner_hp = process_delegators(delegators_list, partner_accounts)
    
    delegators.insert(0, {"Account": receiver_account, "Delegated HP": own_hp})
    delegators.insert(1, {"Account": "Partner Accounts", "Delegated HP": partner_hp})

    save_delegators_to_xlsx(delegators, earnings)

if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv
from modules.fetch_delegators import fetch_delegators
from modules.account_info import get_account_info, vests_to_hp
from modules.partners_info import get_partner_accounts
from modules.save_to_csv import save_delegators_to_csv

# Carregar variáveis de ambiente
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
        hp_delegado = vests_to_hp(vesting_shares)
        if delegator in partner_accounts:
            partner_hp += hp_delegado
        else:
            delegators.append({
                "Conta": delegator,
                "HP Delegado": hp_delegado
            })
    
    delegators.insert(0, {"Conta": receiver_account, "HP Delegado": own_hp})
    delegators.insert(1, {"Conta": "Contas Parceiras", "HP Delegado": partner_hp})

    save_delegators_to_csv(delegators)

if __name__ == "__main__":
    main()

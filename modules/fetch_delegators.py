import requests
import pandas as pd
import os
from dotenv import load_dotenv
from beem import Hive
from beem.account import Account

load_dotenv()

def fetch_delegators():
    hive = Hive()
    receiver_account = os.getenv("RECEIVER_ACCOUNT")
    partner_accounts = os.getenv("PARTNER_ACCOUNTS").split(',')

    account = Account(receiver_account, blockchain_instance=hive)
    
    # Obtendo o HP total e o HP delegado
    total_vests = float(account['vesting_shares'].amount)
    delegated_vests = float(account['delegated_vesting_shares'].amount)
    
    # Calculando o HP próprio (Power Up) excluindo o HP delegado
    own_vests = total_vests - delegated_vests
    own_hp = hive.vests_to_hp(own_vests)

    url = f"https://ecency.com/private-api/received-vesting/{receiver_account}"
    response = requests.get(url)
    data = response.json()

    delegators_list = data['list']

    partner_hp = 0
    delegators = []
    for item in delegators_list:
        delegator = item['delegator']
        vesting_shares = float(item['vesting_shares'].replace(' VESTS', ''))
        hp_delegado = hive.vests_to_hp(vesting_shares)
        if delegator in partner_accounts:
            partner_hp += hp_delegado
        else:
            delegators.append({
                "Conta": delegator,
                "HP Delegado": hp_delegado
            })

    # Adicionando a própria conta no topo da lista
    delegators.insert(0, {"Conta": receiver_account, "HP Delegado": own_hp})
    # Adicionando a linha de contas parceiras
    delegators.insert(1, {"Conta": "Contas Parceiras", "HP Delegado": partner_hp})

    df = pd.DataFrame(delegators)
    df.to_csv("data/delegators.csv", index=False)
    print("Lista de delegadores salva com sucesso em 'data/delegators.csv'.")

if __name__ == "__main__":
    fetch_delegators()
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_delegators(receiver_account):
    url = f"https://ecency.com/private-api/received-vesting/{receiver_account}"
    response = requests.get(url)
    data = response.json()
    return data['list']

def fetch_delegators():
    receiver_account = os.getenv("RECEIVER_ACCOUNT")
    return get_delegators(receiver_account)

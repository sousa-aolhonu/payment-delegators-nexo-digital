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
    url = f"https://ecency.com/private-api/received-vesting/{receiver_account}"
    
    response = requests.get(url)
    data = response.json()

    delegators_list = data['list']

    delegators = []
    for item in delegators_list:
        delegator = item['delegator']
        vesting_shares = float(item['vesting_shares'].replace(' VESTS', ''))
        hp_delegado = hive.vests_to_hp(vesting_shares)
        delegators.append({
            "Conta": delegator,
            "HP Delegado": hp_delegado
        })

    df = pd.DataFrame(delegators)
    df.to_csv("data/delegators.csv", index=False)
    print("Lista de delegadores salva com sucesso em 'data/delegators.csv'.")

if __name__ == "__main__":
    fetch_delegators()

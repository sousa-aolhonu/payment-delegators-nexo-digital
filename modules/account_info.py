from beem import Hive
from beem.account import Account

def get_account_info(account_name):
    try:
        hive = Hive()
        account = Account(account_name, blockchain_instance=hive)
        total_vests = float(account['vesting_shares'].amount)
        delegated_vests = float(account['delegated_vesting_shares'].amount)
        own_vests = total_vests - delegated_vests
        own_hp = hive.vests_to_hp(own_vests)
        print(f"[Success] Fetched account info for {account_name}.")
        return own_hp
    except Exception as e:
        print(f"[Error] Error getting account info for {account_name}: {e}")
        return 0

def vests_to_hp(vesting_shares):
    try:
        hive = Hive()
        hp = hive.vests_to_hp(vesting_shares)
        print(f"[Success] Converted vests to HP.")
        return hp
    except Exception as e:
        print(f"[Error] Error converting vests to HP: {e}")
        return 0

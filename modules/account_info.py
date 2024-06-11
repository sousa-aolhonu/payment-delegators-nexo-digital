from beem import Hive
from beem.account import Account

def get_account_info(account_name):
    hive = Hive()
    account = Account(account_name, blockchain_instance=hive)
    
    total_vests = float(account['vesting_shares'].amount)
    delegated_vests = float(account['delegated_vesting_shares'].amount)
    
    own_vests = total_vests - delegated_vests
    own_hp = hive.vests_to_hp(own_vests)
    
    return own_hp

def vests_to_hp(vesting_shares):
    hive = Hive()
    return hive.vests_to_hp(vesting_shares)

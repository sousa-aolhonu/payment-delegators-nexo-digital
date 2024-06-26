import logging
from beem import Hive
from beem.account import Account
from colorama import Fore, Style, init

init(autoreset=True)


def get_account_info(account_name):
    try:
        print(
            f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching account info for {Fore.BLUE}{account_name}{Style.RESET_ALL}..."
        )
        hive = Hive()
        account = Account(account_name, blockchain_instance=hive)
        total_vests = float(account["vesting_shares"].amount)
        delegated_vests = float(account["delegated_vesting_shares"].amount)
        own_vests = total_vests - delegated_vests
        own_hp = hive.vests_to_hp(own_vests)
        print(
            f"{Fore.GREEN}[Success]{Style.RESET_ALL} Fetched account info for {Fore.BLUE}{account_name}{Style.RESET_ALL}: {Fore.YELLOW}{own_hp} HP{Style.RESET_ALL}."
        )
        return own_hp
    except Exception as e:
        logging.error(f"Error getting account info for {account_name}: {e}")
        print(
            f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting account info for {Fore.BLUE}{account_name}{Style.RESET_ALL}: {e}"
        )
        return 0


def vests_to_hp(vesting_shares, delegator):
    try:
        print(
            f"{Fore.CYAN}[Info]{Style.RESET_ALL} Converting vests to HP for {Fore.BLUE}{delegator}{Style.RESET_ALL}..."
        )
        hive = Hive()
        hp = hive.vests_to_hp(vesting_shares)
        print(
            f"{Fore.GREEN}[Success]{Style.RESET_ALL} Converted vests to HP for {Fore.BLUE}{delegator}{Style.RESET_ALL}: {Fore.YELLOW}{hp} HP{Style.RESET_ALL}."
        )
        return hp
    except Exception as e:
        logging.error(f"Error converting vests to HP for {delegator}: {e}")
        print(
            f"{Fore.RED}[Error]{Style.RESET_ALL} Error converting vests to HP for {Fore.BLUE}{delegator}{Style.RESET_ALL}: {e}"
        )
        return 0

import os
import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_latest_file(directory, prefix):
    try:
        files = [f for f in os.listdir(directory) if f.startswith(prefix)]
        if not files:
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} No files found.")
            return None
        files.sort(reverse=True)
        latest_file = os.path.join(directory, files[0])
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Latest file found: {Fore.BLUE}{latest_file}{Style.RESET_ALL}")
        return latest_file
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting latest file: {e}")
        return None

def get_previous_own_hp(latest_file, receiver_account):
    try:
        if latest_file:
            df = pd.read_excel(latest_file)
            previous_own_hp = df.loc[df['Account'] == receiver_account, 'Delegated HP'].values[0]
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Previous own HP retrieved.")
            return previous_own_hp
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting previous own HP: {e}")
    return 0

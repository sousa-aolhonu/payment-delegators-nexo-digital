import os
import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_latest_file(directory, prefix):
    """
    Gets the latest file in a directory with the specified prefix.

    Args:
        directory (str): The directory to search for files.
        prefix (str): The prefix of the files to search for.

    Returns:
        str: The path to the latest file, or None if no files are found or an error occurs.
    """
    try:
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Getting the latest file in directory {Fore.BLUE}{directory}{Style.RESET_ALL} with prefix {Fore.BLUE}{prefix}{Style.RESET_ALL}...")
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
    """
    Gets the previous own HP (Hive Power) from the latest file for the specified receiver account.

    Args:
        latest_file (str): The path to the latest file.
        receiver_account (str): The name of the receiver account.

    Returns:
        float: The previous own HP, or 0 if an error occurs.
    """
    try:
        if latest_file:
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Reading latest file {Fore.BLUE}{latest_file}{Style.RESET_ALL} to get previous own HP for {Fore.BLUE}{receiver_account}{Style.RESET_ALL}...")
            df = pd.read_excel(latest_file)
            previous_own_hp = df.loc[df['Account'] == receiver_account, 'Delegated HP'].values[0]
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Previous own HP retrieved: {Fore.YELLOW}{previous_own_hp}{Style.RESET_ALL}")
            return previous_own_hp
    except Exception as e:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error getting previous own HP: {e}")
    return 0

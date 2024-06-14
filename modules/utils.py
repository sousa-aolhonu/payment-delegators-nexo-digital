import os
import pandas as pd

def get_latest_file(directory, prefix):
    try:
        files = [f for f in os.listdir(directory) if f.startswith(prefix)]
        if not files:
            print("[Info] No files found.")
            return None
        files.sort(reverse=True)
        latest_file = os.path.join(directory, files[0])
        print(f"[Success] Latest file found: {latest_file}")
        return latest_file
    except Exception as e:
        print(f"[Error] Error getting latest file: {e}")
        return None

def get_previous_own_hp(latest_file, receiver_account):
    try:
        if latest_file:
            df = pd.read_excel(latest_file)
            previous_own_hp = df.loc[df['Account'] == receiver_account, 'Delegated HP'].values[0]
            print("[Success] Previous own HP retrieved.")
            return previous_own_hp
    except Exception as e:
        print(f"[Error] Error getting previous own HP: {e}")
    return 0

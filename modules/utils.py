import os
import pandas as pd

def get_latest_file(directory, prefix):
    """Get the latest file from the specified directory with the given prefix."""
    files = [f for f in os.listdir(directory) if f.startswith(prefix)]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(directory, files[0])

def get_previous_own_hp(latest_file, receiver_account):
    """Extract the own HP of the receiver account from the latest file."""
    if latest_file:
        df = pd.read_csv(latest_file)
        previous_own_hp = df.loc[df['Account'] == receiver_account, 'Delegated HP'].values[0]
        return previous_own_hp
    return 0

import pandas as pd

def save_delegators_to_csv(delegators, filename="data/delegators.csv"):
    df = pd.DataFrame(delegators)
    df.to_csv(filename, index=False)
    print(f"Lista de delegadores salva com sucesso em '{filename}'.")

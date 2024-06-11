import pandas as pd
from datetime import datetime

def save_delegators_to_csv(delegators):
    # Obter a data e hora atual
    now = datetime.now()
    # Formatar a data e hora no formato especificado
    timestamp = now.strftime("pd_%m-%d-%Y_%H-%M-%S")
    filename = f"data/{timestamp}.csv"
    
    # Salvar o DataFrame como CSV
    df = pd.DataFrame(delegators)
    df.to_csv(filename, index=False)
    print(f"Lista de delegadores salva com sucesso em '{filename}'.")

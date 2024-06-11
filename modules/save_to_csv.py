import pandas as pd
from datetime import datetime

def save_delegators_to_csv(delegators):
    # Get the current date and time
    now = datetime.now()
    # Format the date and time in the specified format
    timestamp = now.strftime("pd_%m-%d-%Y_%H-%M-%S")
    filename = f"data/{timestamp}.csv"
    
    # Create DataFrame
    df = pd.DataFrame(delegators)
    
    # Calculate the percentage column
    total_hp = df["Delegated HP"].sum()
    df["Percentage"] = df["Delegated HP"] / total_hp * 100
    
    # Create a DataFrame for the total row
    total_row = pd.DataFrame([{
        "Account": "Total",
        "Delegated HP": total_hp,
        "Percentage": 100
    }])
    
    # Concatenate the original DataFrame with the total row
    df = pd.concat([df, total_row], ignore_index=True)
    
    # Save the DataFrame as CSV
    df.to_csv(filename, index=False)
    print(f"Delegators list successfully saved in '{filename}'.")

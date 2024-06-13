import pandas as pd
from datetime import datetime

def save_delegators_to_csv(delegators, earnings):
    # Get the current date and time
    now = datetime.now()
    # Format the date and time in the specified format
    timestamp = now.strftime("pd_%m-%d-%Y_%H-%M-%S")
    filename = f"data/{timestamp}.csv"
    
    # Create DataFrame
    df = pd.DataFrame(delegators)
    
    # Round the values to 3 decimal places
    df["Delegated HP"] = df["Delegated HP"].round(3)
    
    # Calculate the percentage column
    total_hp = df["Delegated HP"].sum().round(3)
    df["Percentage"] = (df["Delegated HP"] / total_hp * 100).round(3)
    
    # Create a DataFrame for the total row
    total_row = pd.DataFrame([{
        "Account": "Total",
        "Delegated HP": total_hp,
        "Percentage": 100.000
    }])
    
    # Concatenate the original DataFrame with the total row
    df = pd.concat([df, total_row], ignore_index=True)
    
    # Add Earnings for the period row
    earnings_row = pd.DataFrame([{
        "Account": "Earnings for the period",
        "Delegated HP": round(earnings, 3),
        "Percentage": ""
    }])
    
    df = pd.concat([df, earnings_row], ignore_index=True)
    
    # Save the DataFrame as CSV
    df.to_csv(filename, index=False)
    print(f"Delegators list successfully saved in '{filename}'.")

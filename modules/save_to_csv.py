import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

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
    
    # Calculate HIVE Deduction
    hive_deduction_multiplier = float(os.getenv("HIVE_DEDUCTION_MULTIPLIER", 2))
    df["HIVE Deduction"] = (df["Percentage"] * earnings * hive_deduction_multiplier / 100).round(3)
    
    # Calculate TOKEN_NAME Payment
    token_name = os.getenv("TOKEN_NAME", "NEXO")
    token_fixed_price = float(os.getenv("TOKEN_FIXED_PRICE", 0.1))
    df[f"{token_name} Payment"] = ((df["HIVE Deduction"] * token_fixed_price) * 100).round(3)
    
    # Calculate totals
    total_hive_deduction = df["HIVE Deduction"].sum().round(3)
    total_token_payment = df[f"{token_name} Payment"].sum().round(3)
    
    # Create a DataFrame for the total row
    total_row = pd.DataFrame([{
        "Account": "Total",
        "Delegated HP": total_hp,
        "Percentage": 100.000,
        "HIVE Deduction": total_hive_deduction,
        f"{token_name} Payment": total_token_payment
    }])
    
    # Concatenate the original DataFrame with the total row
    df = pd.concat([df, total_row], ignore_index=True)
    
    # Add Earnings for the period row
    earnings_row = pd.DataFrame([{
        "Account": "Earnings for the period",
        "Delegated HP": round(earnings, 3),
        "Percentage": "",
        "HIVE Deduction": "",
        f"{token_name} Payment": ""
    }])
    
    df = pd.concat([df, earnings_row], ignore_index=True)
    
    # Save the DataFrame as CSV
    df.to_csv(filename, index=False)
    print(f"Delegators list successfully saved in '{filename}'.")

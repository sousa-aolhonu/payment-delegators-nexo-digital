from colorama import Fore, Style
from modules.wallet_utils import check_balance, wait_for_transaction, wait_for_transaction_id
from modules.memo_utils import generate_unique_hash, format_memo, get_current_date
import logging

def process_payment_for_delegator(wallet, payment_account, token_name, delegator, payment_amount, df, index):
    """
    Processes a payment for a specific delegator.

    Args:
        wallet (HiveEngineWallet): The Hive Engine wallet to use for the payment.
        payment_account (Account): The Hive account making the payment.
        token_name (str): The name of the token to be paid.
        delegator (str): The name of the delegator receiving the payment.
        payment_amount (float): The amount of tokens to be paid.
        df (pd.DataFrame): The DataFrame containing delegator information.
        index (int): The index of the delegator in the DataFrame.

    Returns:
        bool: True if the payment was processed successfully, False otherwise.
    """
    try:
        logging.info(f"Checking initial balance...")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Checking initial balance...")
        initial_balance = check_balance(wallet)
        logging.info(f"Initial balance: {initial_balance}")
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Initial balance: {Fore.YELLOW}{initial_balance}")

        if payment_amount <= initial_balance:
            current_date = get_current_date()
            unique_hash = generate_unique_hash(delegator, payment_amount, current_date)
            memo = format_memo(delegator, payment_amount, current_date, unique_hash)
            logging.info(f"Initiating reward of {payment_amount} {token_name} to {delegator} with memo: {memo}")
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Initiating reward of {Fore.YELLOW}{payment_amount} {token_name}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL} with memo: {memo}...")
            
            wallet.transfer(delegator, str(f"{payment_amount:.3f}"), token_name, memo)
            logging.info(f"Reward of {payment_amount} {token_name} to {delegator} completed successfully.")
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Reward of {Fore.YELLOW}{payment_amount}{Style.RESET_ALL} {token_name} to {Fore.BLUE}{delegator}{Style.RESET_ALL} completed successfully.")

            logging.info("Waiting for transaction to be reflected in the blockchain...")
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Waiting for transaction to be reflected in the blockchain...")
            final_balance = wait_for_transaction(wallet, initial_balance, payment_amount)
            if final_balance is not None:
                logging.info(f"Transaction reflected in the blockchain. Final balance: {final_balance}")
                print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Transaction reflected in the blockchain. Final balance: {Fore.YELLOW}{final_balance}")

                logging.info(f"Fetching transaction ID...")
                print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Fetching transaction ID...")
                txid = wait_for_transaction_id(payment_account.name, delegator, payment_amount, token_name)
                if txid:
                    df.at[index, "TxID"] = txid
                    df.at[index, "Unique Hash"] = unique_hash
                    logging.info(f"Transaction ID for {delegator}: {txid}")
                    print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Transaction ID for {Fore.BLUE}{delegator}{Style.RESET_ALL}: {Fore.YELLOW}{txid}")
                else:
                    df.at[index, "TxID"] = "Not found"
                return True
            else:
                logging.error(f"Failed to confirm transaction for {delegator}.")
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Failed to confirm transaction for {Fore.BLUE}{delegator}{Style.RESET_ALL}.")
                df.at[index, "TxID"] = "Failed"
                return False
        else:
            logging.error(f"Insufficient balance to reward {payment_amount} {token_name} to {delegator}.")
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Insufficient balance to reward {Fore.YELLOW}{payment_amount}{Style.RESET_ALL} {token_name} to {Fore.BLUE}{delegator}{Style.RESET_ALL}.")
            return False
    except Exception as e:
        logging.error(f"Error processing reward for {delegator}: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error processing reward for {Fore.BLUE}{delegator}{Style.RESET_ALL}: {e}")
        df.at[index, "TxID"] = "Error"
        return False

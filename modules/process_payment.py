from colorama import Fore, Style
from modules.wallet_utils import check_balance, wait_for_transaction, wait_for_transaction_id

def process_payment_for_delegator(wallet, payment_account, token_name, delegator, payment_amount, df, index):
    initial_balance = check_balance(wallet)
    if payment_amount <= initial_balance:
        wallet.transfer(delegator, str(f"{payment_amount:.3f}"), token_name, "Delegation payment")
        print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Payment of {Fore.YELLOW}{payment_amount}{Style.RESET_ALL} {Fore.YELLOW}{token_name}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL} completed successfully.")
        # Wait for the transaction to be reflected in the blockchain
        final_balance = wait_for_transaction(wallet, initial_balance, payment_amount)
        if final_balance is not None:
            txid = wait_for_transaction_id(payment_account.name, delegator, payment_amount, token_name)
            df.at[index, "TxID"] = txid if txid else "Not found"
            return True
        else:
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Failed to confirm transaction for {Fore.BLUE}{delegator}{Style.RESET_ALL}.")
            return False
    else:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Insufficient balance to pay {Fore.YELLOW}{payment_amount}{Style.RESET_ALL} {Fore.YELLOW}{token_name}{Style.RESET_ALL} to {Fore.BLUE}{delegator}{Style.RESET_ALL}.")
        return False

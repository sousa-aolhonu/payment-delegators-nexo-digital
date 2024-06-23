import logging
import os
from colorama import Fore, Style

def setup_logging(timestamp, log_dir='data/log', log_filename=None):
    if log_filename is None:
        log_filename = f'log_{timestamp}.txt'

    os.makedirs(log_dir, exist_ok=True)
    
    log_file_path = os.path.join(log_dir, log_filename)
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Setting up logging. Log file: {Fore.BLUE}{log_file_path}{Style.RESET_ALL}")

    logging.basicConfig(
        filename=log_file_path,
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    logging.info("Logging setup complete.")
    print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Logging setup complete.")

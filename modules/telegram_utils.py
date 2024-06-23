import os
import logging
import requests
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()

def send_telegram_file(file_path, caption):
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            logging.error("Telegram bot token or chat ID not set in environment variables.")
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Telegram bot token or chat ID not set in environment variables.")
            return False

        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        with open(file_path, 'rb') as file:
            response = requests.post(url, data={'chat_id': chat_id, 'caption': caption}, files={'document': file})
        
        if response.status_code == 200:
            logging.info("Log file sent successfully to Telegram.")
            print(f"{Fore.GREEN}[Success]{Style.RESET_ALL} Log file sent successfully to Telegram.")
            return True
        else:
            logging.error(f"Failed to send log file to Telegram: {response.status_code} {response.text}")
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Failed to send log file to Telegram: {response.status_code} {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error sending log file to Telegram: {e}")
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Error sending log file to Telegram: {e}")
        return False

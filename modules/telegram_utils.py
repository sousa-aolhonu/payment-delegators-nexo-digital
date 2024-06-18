import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

def send_telegram_file(file_path, caption):
    """
    Sends a file to a Telegram chat.

    Args:
        file_path (str): The path to the file to send.
        caption (str): The caption to include with the file.

    Returns:
        bool: True if the file was sent successfully, False otherwise.
    """
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            logging.error("Telegram bot token or chat ID not set in environment variables.")
            return False

        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        with open(file_path, 'rb') as file:
            response = requests.post(url, data={'chat_id': chat_id, 'caption': caption}, files={'document': file})
        
        if response.status_code == 200:
            logging.info("Log file sent successfully to Telegram.")
            return True
        else:
            logging.error(f"Failed to send log file to Telegram: {response.status_code} {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error sending log file to Telegram: {e}")
        return False

import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()


def send_discord_file(file_path, message):
    try:
        bot_token = os.getenv("DISCORD_BOT_TOKEN")
        channel_id = os.getenv("DISCORD_CHANNEL_ID")

        if not bot_token or not channel_id:
            logging.error(
                "Discord bot token or channel ID not set in environment variables."
            )
            return False

        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        headers = {"Authorization": f"Bot {bot_token}"}
        data = {"content": message}
        files = {"file": (os.path.basename(file_path), open(file_path, "rb"))}

        response = requests.post(url, headers=headers, data=data, files=files)

        if response.status_code == 200:
            logging.info("Spreadsheet file sent successfully to Discord.")
            return True
        else:
            logging.error(
                f"Failed to send spreadsheet file to Discord: {response.status_code} {response.text}"
            )
            return False
    except Exception as e:
        logging.error(f"Error sending spreadsheet file to Discord: {e}")
        return False

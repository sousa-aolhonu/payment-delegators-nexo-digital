from dotenv import load_dotenv
import os
import logging
from colorama import Fore, Style

load_dotenv()


def check_env_variables():
    required_vars = [
        "RECEIVER_ACCOUNT",
        "PAYMENT_ACCOUNT",
        "HIVE_ENGINE_ACTIVE_PRIVATE_KEY",
        "HIVE_ENGINE_POSTING_PRIVATE_KEY",
        "TOKEN_NAME",
        "TOKEN_FIXED_PRICE",
        "HIVE_DEDUCTION_MULTIPLIER",
        "ACTIVATE_PAYMENTS",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "DISCORD_BOT_TOKEN",
        "DISCORD_CHANNEL_ID",
    ]
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            logging.error(f"Environment variable {var} is not set")
            print(
                f"{Fore.RED}[Error]{Style.RESET_ALL} Environment variable {Fore.BLUE}{var}{Style.RESET_ALL} is not set"
            )

    if missing_vars:
        raise EnvironmentError(
            f"Environment variables not set: {', '.join(missing_vars)}"
        )

    logging.info(f"All required environment variables are set.")
    print(
        f"{Fore.GREEN}[Success]{Style.RESET_ALL} All required environment variables are set."
    )

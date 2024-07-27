import schedule
import time
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


def run_main_script():
    print("Runing payment-delegators-nexo-digital")
    subprocess.call(["python", "main.py"])
    print("payment-delegators-nexo-digital executed.")


def job():
    run_main_script()


def next_run_time():
    next_run = schedule.jobs[0].next_run if schedule.jobs else None
    if next_run:
        now = datetime.now()
        time_diff = next_run - now
        return time_diff
    return None


schedule_time = os.getenv("SCHEDULE_TIME", "00:00")
hour, minute = map(int, schedule_time.split(":"))

schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(job)

print(
    f"Scheduling initialized. payment-delegators-nexo-digital will run daily at {hour:02d}:{minute:02d}."
)

while True:
    schedule.run_pending()
    time_to_next_run = next_run_time()
    if time_to_next_run:
        print(
            f"Time remaining for next run [payment-delegators-nexo-digital]: {time_to_next_run}"
        )
    else:
        print("No executions scheduled.")
    time.sleep(1)

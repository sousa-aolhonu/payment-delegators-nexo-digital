import schedule
import time
import subprocess
from datetime import datetime


def run_main_script():
    print("Runing payment-delegrators-nexo-digital")
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


schedule.every(10).minutes.do(job)

print("Scheduling initialized. The test will run every 10 minute.")

while True:
    schedule.run_pending()
    time_to_next_run = next_run_time()
    if time_to_next_run:
        print(f"Time remaining for next run: {time_to_next_run}")
    else:
        print("No executions scheduled.")
    time.sleep(1)

import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

def write_log(ticker: str, message: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(LOGS_DIR, f"{ticker}.log")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")
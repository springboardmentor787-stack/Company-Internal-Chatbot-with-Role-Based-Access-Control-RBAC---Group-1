import logging
from datetime import datetime
from pathlib import Path

# Create log file inside backend folder
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "access.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_access(username, role, department, status):
    logging.info(
        f"User: {username} | Role: {role} | Dept: {department} | Status: {status}"
    )

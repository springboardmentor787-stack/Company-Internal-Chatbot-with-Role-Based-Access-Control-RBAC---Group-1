import os
import json
from datetime import datetime

LOG_PATH = "data/access.log"

def log_event(username, role, question, answer, confidence, status):

    os.makedirs("data", exist_ok=True)

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "role": role,
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "status": status
    }

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data) + "\n")

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "roles_config.json"


def load_role_mapping():
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        role_mapping = json.load(f)

    return role_mapping


  


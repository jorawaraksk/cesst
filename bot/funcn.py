import json
from pathlib import Path

MODE_FILE = Path("mode.json")

def load_mode():
    if MODE_FILE.exists():
        try:
            with open(MODE_FILE) as f:
                return json.load(f).get("is_public", True)
        except:
            return True
    return True

def save_mode(state):
    with open(MODE_FILE, "w") as f:
        json.dump({"is_public": state}, f)

IS_PUBLIC = load_mode()

def is_authorized(user_id):
    return IS_PUBLIC or str(user_id) in OWNER or user_id == DEV

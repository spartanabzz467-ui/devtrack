"""File I/O utilities — load and save all data to/from JSON."""

import json
import os
from models.user import User

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "devtrack_data.json")


def _ensure_data_dir():
    """Create the data directory if it doesn't exist."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def load_users() -> list[User]:
    """Load all users from the JSON data file. Returns empty list if file missing."""
    _ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [User.from_dict(u) for u in raw.get("users", [])]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[Warning] Could not read data file: {e}. Starting fresh.")
        return []


def save_users(users: list[User]):
    """Persist all users (with their projects and tasks) to the JSON data file."""
    _ensure_data_dir()
    data = {"users": [u.to_dict() for u in users]}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def find_user(users: list[User], name: str) -> User | None:
    """Find a user by name (case-insensitive)."""
    return next((u for u in users if u.name.lower() == name.lower()), None)

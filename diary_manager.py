import json
import os
from datetime import datetime

DIARY_FILE = "diary_data.json"

def load_data():
    """Load the entire diary data from JSON file."""
    if not os.path.exists(DIARY_FILE):
        return {}
    
    try:
        with open(DIARY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_entry(date_str, data):
    """
    Save or update an entry for a specific date.
    
    Args:
        date_str (str): Date string in YYYY-MM-DD format.
        data (dict): Dictionary containing diary text and answers.
                     e.g. {'happy_text': '...', 'hard_text': '...', 'answers': {...}}
    """
    all_data = load_data()
    
    # Update logic: simpler to just overwrite the day's entry with new data
    # but we might want to preserve other fields if we add them later.
    # For now, simplistic update.
    
    data["last_updated"] = datetime.now().isoformat()
    all_data[date_str] = data
    
    with open(DIARY_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

def get_entry(date_str):
    """Get entry for a specific date. Returns None if not found."""
    all_data = load_data()
    return all_data.get(date_str)

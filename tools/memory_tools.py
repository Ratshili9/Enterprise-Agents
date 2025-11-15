import json
import os
from config import MEMORY_FILE

def read_memory_bank() -> dict:
    """Reads the JSON long-term memory file."""
    if not os.path.exists(MEMORY_FILE):
        return {"past_insights": []}
    with open(MEMORY_FILE, 'r') as f:
        print(f"--- [TOOL:Memory] Reading {MEMORY_FILE} ---")
        return json.load(f)

def write_memory_bank(new_entry: str):
    """Writes a new insight entry to the long-term memory file."""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    memory = read_memory_bank()
    
    # We'll just store the date and the new insight
    import datetime
    memory['past_insights'].append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "insight": new_entry
    })
    
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)
        print(f"--- [TOOL:Memory] New insight written to {MEMORY_FILE} ---")
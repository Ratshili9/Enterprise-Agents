import json
import os
import time

MEMORY_FILE = os.path.join("reports", "memory_bank.json")
MAX_INSIGHTS = 10  # Limit the size of the memory bank


def read_memory_bank() -> list[dict]:
    """
    Reads the list of past insights from the memory bank JSON file.

    Returns:
        A list of insight dictionaries, or an empty list on failure.
    """
    print(f"--- [TOOL:Memory] Reading {MEMORY_FILE} ---")
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure the loaded structure is a list under 'past_insights'
            return data.get('past_insights', [])
    except Exception as e:
        print(f"Memory Tool Error: Could not read memory bank: {e}")
        # Re-initialize the file if it's corrupted
        initialize_memory_bank()
        return []


def write_insight_to_memory(insight: str, source: str, date: str = None):
    """
    Adds a new insight to the memory bank and maintains the maximum size.

    Args:
        insight: The text of the new finding.
        source: The agent that generated the insight (e.g., 'InternalInsightsAgent').
        date: The date/time of the insight (defaults to current time).
    """
    if not insight or not source:
        print("Memory Tool Warning: Insight or source cannot be empty.")
        return

    past_insights = read_memory_bank()

    new_record = {
        "date": date if date else time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "insight": insight
    }

    # Add new record and enforce max size (oldest records are dropped)
    past_insights.append(new_record)
    # Keep only the last MAX_INSIGHTS
    past_insights = past_insights[-MAX_INSIGHTS:]

    try:
        data = {"past_insights": past_insights}
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"--- [TOOL:Memory] New insight written to {MEMORY_FILE} ---")
    except Exception as e:
        print(f"Memory Tool Error: Could not write memory bank: {e}")


def initialize_memory_bank():
    """Ensures the memory bank file exists and is correctly initialized."""
    if not os.path.exists(MEMORY_FILE):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        try:
            with open(MEMORY_FILE, "w", encoding='utf-8') as f:
                f.write('{"past_insights": []}')
        except Exception as e:
            print(
                f"Memory Tool Error: Could not initialize memory bank file: {e}")

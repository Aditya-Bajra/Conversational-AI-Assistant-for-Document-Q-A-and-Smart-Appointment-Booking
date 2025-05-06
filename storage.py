import json
import os

def save_booking(entry, filepath="data/appointments.json"):
    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    data.append(entry)

    with open(filepath, "w") as f:
        json.dump(data, f, indent = 2)
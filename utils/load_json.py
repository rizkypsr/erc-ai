import json
import os


def load_json(filename):
    try:
        current_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(current_dir, filename)

        # Open and read the JSON file
        with open(file_path, "r") as file:
            coins = json.load(file)

        return coins
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file: {e}")
        return None

import json
import os

class BaseRepository:
    def __init__(self, entity_name, data_file="data/banks.json"):
        self.entity_name = entity_name
        self.data_file = data_file
        self._ensure_data_file_exists()

    def _ensure_data_file_exists(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({
                    "bank": [],
                    "staff_members": [],
                    "accounts": [],
                    "transactions": [],
                    "currencies": [],
                    "charges": []
                }, f, indent=4)

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            return data.get(self.entity_name, [])
        except json.JSONDecodeError:
            print(f"Error: The file {self.data_file} contains invalid JSON. Returning empty data.")
            return []
        except FileNotFoundError:
            print(f"Error: The file {self.data_file} was not found. Returning empty data.")
            return []

    def save_data(self, items):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            data[self.entity_name] = items
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
        except json.JSONDecodeError:
            print(f"Error: The file {self.data_file} contains invalid JSON. Data could not be saved.")
        except Exception as e:
            print(f"An error occurred while saving data to {self.data_file}: {e}")

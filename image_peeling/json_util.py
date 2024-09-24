import json
import os


class JsonUtil:
    def __init__(self, config_path: str) -> None:
        self.config_path = os.path.abspath(config_path)
        self.load_json()

    def load_json(self):
        with open(self.config_path) as f:
            self.config = json.load(f)

    def save_json(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

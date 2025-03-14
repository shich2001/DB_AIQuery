import json
import os

CONFIG_FILE = "config.json"

class Config:
    def __init__(self):
        self.postgresql = {
            "host": "localhost",
            "port": 5432,
            "database": "your_database",
            "user": "your_username",
            "password": "",
        }
        self.openai = {
            "api_base_url": "https://api.openai.com/v1",
            "api_key": "",
            "model": "gpt-3.5-turbo",
        }
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                self.postgresql = config.get("postgresql", self.postgresql)
                self.openai = config.get("openai", self.openai)

    def save(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(
                {"postgresql": self.postgresql, "openai": self.openai},
                f,
                indent=4,
            )

    def get_postgresql_config(self):
        return self.postgresql

    def get_openai_config(self):
        return self.openai
# athena/utils/settings_manager.py

import json
import os

class SettingsManager:
    def __init__(self, settings_file):
        self.settings_file = settings_file

    def load_settings(self):
        if not os.path.exists(self.settings_file):
            default_settings = self.get_default_settings()
            self.save_settings(default_settings)
            return default_settings
        
        try:
            with open(self.settings_file, 'r') as f:
                content = f.read().strip()
                if not content:  # File is empty
                    default_settings = self.get_default_settings()
                    self.save_settings(default_settings)
                    return default_settings
                return json.loads(content)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.settings_file}. Using default settings.")
            default_settings = self.get_default_settings()
            self.save_settings(default_settings)
            return default_settings

    def save_settings(self, settings):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

    def get_default_settings(self):
        return {
            "ollama_url": "http://localhost:11434",
            "working_directory": os.path.expanduser("~/Athena_Workspace"),
            "theme": "light_blue.xml"
        }

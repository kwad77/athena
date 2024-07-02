# athena/utils/settings_manager.py

import os
import json

class SettingsManager:
    def __init__(self, working_directory):
        self.working_directory = working_directory
        self.settings_file = os.path.join(self.working_directory, "settings.json")

    def save_settings(self, settings):
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return {}

    def set_working_directory(self, new_directory):
        self.working_directory = new_directory
        self.settings_file = os.path.join(self.working_directory, "settings.json")
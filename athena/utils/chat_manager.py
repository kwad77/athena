# athena/utils/chat_manager.py
import os
import json
from datetime import datetime

class ChatManager:
    def __init__(self, working_directory):
        self.working_directory = working_directory
        self.chats_directory = os.path.join(working_directory, 'chats')
        os.makedirs(self.chats_directory, exist_ok=True)

    def save_chat(self, chat_id, chat_name, messages):
        file_name = f"{chat_id}_{chat_name}.json"
        file_path = os.path.join(self.chats_directory, file_name)
        with open(file_path, 'w') as f:
            json.dump([msg.__dict__ for msg in messages], f, indent=4, default=str)

    def load_chat(self, file_name):
        file_path = os.path.join(self.chats_directory, file_name)
        with open(file_path, 'r') as f:
            return json.load(f)

    def list_chats(self):
        return [f for f in os.listdir(self.chats_directory) if f.endswith('.json')]

    def rename_chat(self, old_name, new_name):
        old_path = os.path.join(self.chats_directory, old_name)
        new_path = os.path.join(self.chats_directory, new_name)
        os.rename(old_path, new_path)

    def set_working_directory(self, new_directory):
        self.working_directory = new_directory
        self.chats_directory = os.path.join(new_directory, 'chats')
        os.makedirs(self.chats_directory, exist_ok=True)
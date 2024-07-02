from typing import List, Dict

class ChatMessage:
    def __init__(self, content: str, sender: str):
        self.content = content
        self.sender = sender

class Chat:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.messages: List[ChatMessage] = []

    def add_message(self, message: ChatMessage):
        self.messages.append(message)
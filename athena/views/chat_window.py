# athena/views/chat_window.py

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextBrowser, QTextEdit, QPushButton, 
                             QComboBox, QLabel, QHBoxLayout, QFileDialog, QApplication)
from PyQt6.QtCore import pyqtSignal, Qt, QBuffer, QByteArray, QIODevice, QUrl
from PyQt6.QtGui import QImage, QPixmap, QKeyEvent, QDesktopServices
from datetime import datetime
import base64

class ChatMessage:
    def __init__(self, content, sender, timestamp=None, content_type='text'):
        self.content = content
        self.sender = sender
        self.timestamp = timestamp or datetime.now()
        self.content_type = content_type  # 'text', 'image', or 'document'

class PasteAwareTextEdit(QTextEdit):
    image_pasted = pyqtSignal(str, str)  # signal emits file_path, content_type

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.parent().send_message()
        else:
            super().keyPressEvent(event)

    def insertFromMimeData(self, source):
        if source.hasImage():
            image = QImage(source.imageData())
            if not image.isNull():
                # Save the image to a temporary file
                temp_path = os.path.join(os.path.expanduser("~"), "temp_pasted_image.png")
                image.save(temp_path, "PNG")
                self.image_pasted.emit(temp_path, "image")
            else:
                super().insertFromMimeData(source)
        elif source.hasUrls():
            for url in source.urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    self.image_pasted.emit(file_path, "image")
                else:
                    self.insertPlainText(file_path)
        elif source.hasText():
            self.insertPlainText(source.text())
        else:
            super().insertFromMimeData(source)

class ChatWindow(QWidget):
    message_sent = pyqtSignal(str, str)
    new_chat_requested = pyqtSignal()
    document_uploaded = pyqtSignal(str)
    model_changed = pyqtSignal(str)
    export_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = None
        self.chat_history = []
        self.current_document = None
        self.init_ui()

    def set_controller(self, controller):
        self.controller = controller

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Model selector
        model_layout = QHBoxLayout()
        self.model_selector = QComboBox()
        self.model_selector.currentTextChanged.connect(self.on_model_changed)
        model_layout.addWidget(QLabel("Model:"))
        model_layout.addWidget(self.model_selector)
        layout.addLayout(model_layout)

        # Chat display
        self.chat_display = QTextBrowser()
        self.chat_display.setOpenExternalLinks(True)
        layout.addWidget(self.chat_display)

        # Message input
        self.message_input = PasteAwareTextEdit()
        self.message_input.setPlaceholderText("Type your message here... (Ctrl+V to paste images)")
        self.message_input.setFixedHeight(60)
        self.message_input.image_pasted.connect(self.handle_pasted_image)
        layout.addWidget(self.message_input)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        # Additional buttons
        button_layout = QHBoxLayout()
        self.new_chat_button = QPushButton("New Chat")
        self.new_chat_button.clicked.connect(self.request_new_chat)
        self.upload_button = QPushButton("Upload Document")
        self.upload_button.clicked.connect(self.upload_document)
        self.export_button = QPushButton("Export Chat")
        self.export_button.clicked.connect(self.export_chat)
        button_layout.addWidget(self.new_chat_button)
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.export_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def send_message(self):
        message = self.message_input.toPlainText().strip()
        if message:
            model = self.model_selector.currentText()
            self.display_message("You", message)
            self.message_sent.emit(message, model)
            self.message_input.clear()

    def handle_pasted_image(self, file_path, content_type):
        if content_type == "image":
            self.display_message("You", file_path, content_type='image')
            with open(file_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            self.message_sent.emit(f"[IMAGE]{base64_image}", self.get_selected_model())

    def display_message(self, sender, content, content_type='text'):
        message = ChatMessage(content, sender, content_type=content_type)
        self.chat_history.append(message)
        self.update_chat_display()

    def update_chat_display(self):
        self.chat_display.clear()
        for message in self.chat_history:
            timestamp = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if message.sender == "You":
                color = "blue"
            elif message.sender == "System":
                color = "red"
            else:
                color = "green"
            
            formatted_message = f'<p style="color: {color};"><b>{message.sender} ({timestamp}):</b> '
            
            if message.content_type == 'text':
                formatted_message += f'{message.content}</p>'
            elif message.content_type == 'image':
                formatted_message += f'[Image: <a href="file:///{message.content}">{os.path.basename(message.content)}</a>]</p>'
                formatted_message += f'<img src="file:///{message.content}" width="200">'
            elif message.content_type == 'document':
                formatted_message += f'[Document: {message.content}]</p>'
            
            self.chat_display.append(formatted_message)
        
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def on_model_changed(self, model):
        self.model_changed.emit(model)

    def request_new_chat(self):
        self.new_chat_requested.emit()
        self.clear_chat()

    def clear_chat(self):
        self.chat_history.clear()
        self.chat_display.clear()
        self.current_document = None

    def upload_document(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Document", "", "Documents (*.pdf *.docx)")
        if file_path:
            self.document_uploaded.emit(file_path)

    def set_document_content(self, file_path, content):
        self.current_document = content
        file_name = os.path.basename(file_path)
        self.display_message("System", f"Document loaded: {file_name}")

    def export_chat(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Chat", "", "Text Files (*.txt)")
        if file_path:
            self.export_requested.emit(file_path)

    def set_model_list(self, models):
        self.model_selector.clear()
        self.model_selector.addItems(models)

    def get_selected_model(self):
        return self.model_selector.currentText()

    def get_current_document(self):
        return self.current_document
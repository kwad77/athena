# athena/controllers/main_controller.py

import logging
import os
from PyQt6.QtWidgets import QMessageBox
from qt_material import apply_stylesheet
from athena.views.main_window import MainWindow
from athena.services.llm_service import LLMService
from athena.services.document_service import DocumentService
from athena.utils.settings_manager import SettingsManager
from athena.config import OLLAMA_BASE_URL, DEFAULT_WORKSPACE

class MainController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing MainController")
        
        self.settings_manager = SettingsManager(DEFAULT_WORKSPACE)
        self.settings = self.settings_manager.load_settings()
        if not self.settings:
            self.settings = {
                "ollama_url": OLLAMA_BASE_URL,
                "working_directory": DEFAULT_WORKSPACE,
                "theme": "light_blue.xml"
            }
            self.settings_manager.save_settings(self.settings)
        
        # Ensure working directory exists
        os.makedirs(self.settings["working_directory"], exist_ok=True)
        
        self.main_window = None
        self.llm_service = LLMService(self.settings["ollama_url"])
        self.document_service = DocumentService(self.settings["working_directory"])
        
        self.init_main_window()
        self.connect_signals()

    def init_main_window(self):
        self.logger.debug("Initializing main window")
        self.main_window = MainWindow()
        self.main_window.set_controller(self)
        self.apply_settings(self.settings)

    def connect_signals(self):
        self.logger.debug("Connecting signals")
        chat_window = self.main_window.chat_window
        chat_window.message_sent.connect(self.handle_message_sent)
        chat_window.new_chat_requested.connect(self.handle_new_chat)
        chat_window.document_uploaded.connect(self.handle_document_upload)
        chat_window.model_changed.connect(self.handle_model_change)
        chat_window.export_requested.connect(self.handle_export_request)

    def apply_settings(self, new_settings):
        self.settings.update(new_settings)
        self.settings_manager.save_settings(self.settings)
        self.llm_service.set_base_url(self.settings["ollama_url"])
        self.document_service.set_working_directory(self.settings["working_directory"])
        if self.main_window:
            apply_stylesheet(self.main_window, theme=self.settings["theme"])
            font = self.main_window.font()
            font.setPointSize(self.settings.get("font_size", 12))
            self.main_window.setFont(font)
        # Apply other settings as needed

    def show_main_window(self):
        self.logger.info("Showing main window")
        self.main_window.show()
        self.load_models()

    def load_models(self):
        self.logger.info("Loading available models")
        try:
            models = self.llm_service.get_available_models()
            self.main_window.chat_window.set_model_list(models)
        except Exception as e:
            self.logger.error(f"Failed to load models: {e}")
            QMessageBox.warning(self.main_window, "Model Loading Error",
                                "Failed to load available models. Please check your connection to Ollama.")

    def handle_message_sent(self, message, model):
        self.logger.info(f"Handling message sent with model: {model}")
        try:
            document_content = self.main_window.chat_window.get_current_document()
            context = f"Document content: {document_content}\n\n" if document_content else ""
            full_prompt = context + message
            response = self.llm_service.generate_response(full_prompt, model)
            self.main_window.chat_window.display_message("Athena", response)
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            self.main_window.chat_window.display_message("Athena", "Sorry, I encountered an error while processing your request.")

    def handle_new_chat(self):
        self.logger.info("Starting a new chat")
        self.main_window.chat_window.clear_chat()

    def handle_document_upload(self, file_path):
        self.logger.info(f"Handling document upload: {file_path}")
        try:
            document_text = self.document_service.process_document(file_path)
            if document_text:
                self.main_window.chat_window.set_document_content(file_path, document_text)
                self.main_window.chat_window.display_message("System", "Document uploaded and processed successfully.")
            else:
                self.main_window.chat_window.display_message("System", "Failed to process the document.")
        except Exception as e:
            self.logger.error(f"Error processing document: {e}")
            self.main_window.chat_window.display_message("System", "An error occurred while processing the document.")
            
    def handle_model_change(self, model):
        self.logger.info(f"Model changed to: {model}")

    def handle_export_request(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for chat in self.main_window.chat_window.chat_history:
                    f.write(f"--- {chat.sender} ({chat.timestamp}) ---\n")
                    f.write(f"{chat.content}\n\n")
            self.logger.info(f"Chat exported to {file_path}")
            QMessageBox.information(self.main_window, "Export Successful", "Chat history has been exported successfully.")
        except Exception as e:
            self.logger.error(f"Error exporting chat: {e}")
            QMessageBox.warning(self.main_window, "Export Error", f"Failed to export chat: {str(e)}")

    def get_working_directory(self):
        return self.settings["working_directory"]

    def set_working_directory(self, directory):
        self.settings["working_directory"] = directory
        self.apply_settings(self.settings)

    def get_ollama_url(self):
        return self.settings["ollama_url"]

    def set_ollama_url(self, url):
        self.settings["ollama_url"] = url
        self.apply_settings(self.settings)

    def get_theme(self):
        return self.settings["theme"]

    def set_theme(self, theme):
        self.settings["theme"] = theme

    def get_font_size(self):
        return self.settings.get("font_size", 12)

    def set_font_size(self, size):
        self.settings["font_size"] = size
        self.apply_settings(self.settings)

    def get_max_tokens(self):
        return self.settings.get("max_tokens", 2000)

    def set_max_tokens(self, tokens):
        self.settings["max_tokens"] = tokens
        self.apply_settings(self.settings)

    def get_temperature(self):
        return self.settings.get("temperature", 0.7)

    def set_temperature(self, temp):
        self.settings["temperature"] = temp
        self.apply_settings(self.settings)

    def save_chat(self, chat_name):
        chat_data = self.main_window.chat_window.chat_history
        file_path = os.path.join(self.get_working_directory(), "chats", f"{chat_name}.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([msg.__dict__ for msg in chat_data], f, indent=2, default=str)
            self.logger.info(f"Chat saved: {chat_name}")
        except Exception as e:
            self.logger.error(f"Error saving chat: {e}")
            raise

    def load_chat(self, chat_name):
        file_path = os.path.join(self.get_working_directory(), "chats", f"{chat_name}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                chat_data = json.load(f)
            self.main_window.chat_window.load_chat_data(chat_data)
            self.logger.info(f"Chat loaded: {chat_name}")
        except Exception as e:
            self.logger.error(f"Error loading chat: {e}")
            raise

    def list_saved_chats(self):
        chat_dir = os.path.join(self.get_working_directory(), "chats")
        os.makedirs(chat_dir, exist_ok=True)
        return [f[:-5] for f in os.listdir(chat_dir) if f.endswith('.json')]

    def delete_chat(self, chat_name):
        file_path = os.path.join(self.get_working_directory(), "chats", f"{chat_name}.json")
        try:
            os.remove(file_path)
            self.logger.info(f"Chat deleted: {chat_name}")
        except Exception as e:
            self.logger.error(f"Error deleting chat: {e}")
            raise

    def handle_settings_update(self, new_settings):
        self.apply_settings(new_settings)
        self.main_window.show_status_message("Settings updated successfully")

    def get_document_content(self, file_path):
        try:
            return self.document_service.get_document_content(file_path)
        except Exception as e:
            self.logger.error(f"Error retrieving document content: {e}")
            return None

    def handle_error(self, error_message):
        self.logger.error(error_message)
        QMessageBox.critical(self.main_window, "Error", error_message)

    def shutdown(self):
        self.logger.info("Shutting down the application")
        # Perform any cleanup or saving operations here
        self.settings_manager.save_settings(self.settings)
        # Close any open resources, connections, etc.        
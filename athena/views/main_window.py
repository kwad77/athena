# athena/views/main_window.py

from PyQt6.QtWidgets import QMainWindow, QStatusBar, QToolBar, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from athena.views.chat_window import ChatWindow
from athena.views.settings_dialog import SettingsDialog
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Athena - Your AI Assistant")
        self.setGeometry(100, 100, 1200, 800)
        self.chat_window = ChatWindow(self)
        self.controller = None

        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Create toolbar
        self.create_toolbar()

        # Create central widget and layout
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.chat_window)
        self.setCentralWidget(self.central_widget)

    def set_controller(self, controller):
        self.controller = controller
        self.chat_window.set_controller(controller)

    def show_status_message(self, message, timeout=5000):
        self.status_bar.showMessage(message, timeout)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        
        # Create settings action with gear icon
        settings_action = QAction(QIcon(self.get_icon_path('gear.png')), 'Settings', self)
        settings_action.triggered.connect(self.show_settings_dialog)
        toolbar.addAction(settings_action)
        
        # You can add more toolbar actions here as needed
        # For example:
        # new_chat_action = QAction(QIcon(self.get_icon_path('new_chat.png')), 'New Chat', self)
        # new_chat_action.triggered.connect(self.chat_window.request_new_chat)
        # toolbar.addAction(new_chat_action)

    def show_settings_dialog(self):
        if self.controller:
            settings_dialog = SettingsDialog(self)
            settings_dialog.set_settings(self.controller.settings)
            if settings_dialog.exec():
                new_settings = settings_dialog.get_settings()
                self.controller.apply_settings(new_settings)

    def get_icon_path(self, icon_name):
        return os.path.join(os.path.dirname(__file__), '..', 'resources', 'icons', icon_name)

    # You can add more methods here as needed, for example:
    # def closeEvent(self, event):
    #     # Handle application closing, maybe save state or show confirmation dialog
    #     event.accept()

    # def resizeEvent(self, event):
    #     # Handle window resizing if needed
    #     super().resizeEvent(event)
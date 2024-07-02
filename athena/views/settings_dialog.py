# athena/views/settings_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFormLayout, QFileDialog,
                             QComboBox, QSpinBox, QCheckBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Athena Settings")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        
        # Ollama URL
        self.ollama_url_input = QLineEdit(self)
        form_layout.addRow("Ollama URL:", self.ollama_url_input)

        # Working Directory
        self.working_dir_input = QLineEdit(self)
        self.working_dir_button = QPushButton("Browse")
        self.working_dir_button.clicked.connect(self.browse_working_dir)
        working_dir_layout = QHBoxLayout()
        working_dir_layout.addWidget(self.working_dir_input)
        working_dir_layout.addWidget(self.working_dir_button)
        form_layout.addRow("Working Directory:", working_dir_layout)

        # Theme
        self.theme_selector = QComboBox(self)
        self.theme_selector.addItems(["light_blue.xml", "dark_blue.xml", "light_red.xml", "dark_red.xml"])
        form_layout.addRow("Theme:", self.theme_selector)

        # Font Size
        self.font_size_input = QSpinBox(self)
        self.font_size_input.setRange(8, 24)
        form_layout.addRow("Font Size:", self.font_size_input)

        # Max Tokens
        self.max_tokens_input = QSpinBox(self)
        self.max_tokens_input.setRange(100, 4000)
        self.max_tokens_input.setSingleStep(100)
        form_layout.addRow("Max Tokens:", self.max_tokens_input)

        # Temperature
        self.temperature_input = QDoubleSpinBox(self)
        self.temperature_input.setRange(0.1, 1.0)
        self.temperature_input.setSingleStep(0.1)
        form_layout.addRow("Temperature:", self.temperature_input)

        # Auto Save
        self.auto_save_checkbox = QCheckBox(self)
        form_layout.addRow("Auto Save:", self.auto_save_checkbox)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_working_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Working Directory")
        if dir_path:
            self.working_dir_input.setText(dir_path)

    def get_settings(self):
        return {
            "ollama_url": self.ollama_url_input.text(),
            "working_directory": self.working_dir_input.text(),
            "theme": self.theme_selector.currentText(),
            "font_size": self.font_size_input.value(),
            "max_tokens": self.max_tokens_input.value(),
            "temperature": self.temperature_input.value(),
            "auto_save": self.auto_save_checkbox.isChecked()
        }

    def set_settings(self, settings):
        self.ollama_url_input.setText(settings.get("ollama_url", ""))
        self.working_dir_input.setText(settings.get("working_directory", ""))
        index = self.theme_selector.findText(settings.get("theme", "light_blue.xml"))
        if index >= 0:
            self.theme_selector.setCurrentIndex(index)
        self.font_size_input.setValue(settings.get("font_size", 12))
        self.max_tokens_input.setValue(settings.get("max_tokens", 2000))
        self.temperature_input.setValue(settings.get("temperature", 0.7))
        self.auto_save_checkbox.setChecked(settings.get("auto_save", True))
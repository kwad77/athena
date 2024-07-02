# main.py
import sys
import os
import importlib
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from athena.controllers.main_controller import MainController
from athena.utils.logging_config import setup_logging
from athena.utils.exceptions import setup_exception_handling
from athena.config import ICON_PATH, APP_NAME, APP_VERSION

def check_dependencies():
    required_modules = ['PyQt6', 'requests', 'PyPDF2', 'docx', 'qt_material']
    missing_modules = []
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError as e:
            missing_modules.append(f"{module}: {str(e)}")
    
    if missing_modules:
        print("Error: The following required modules are missing or have issues:")
        for module in missing_modules:
            print(f"  - {module}")
        print("Please resolve these issues and try again.")
        sys.exit(1)

def main():
    check_dependencies()
    setup_logging()
    
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    setup_exception_handling()
    
    app_icon = QIcon(ICON_PATH)
    app.setWindowIcon(app_icon)
    
    controller = MainController()
    controller.show_main_window()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
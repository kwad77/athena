# athena/utils/exceptions.py
import sys
import traceback
import logging
from PyQt6.QtWidgets import QMessageBox

def global_exception_handler(exctype, value, tb):
    logging.error("Uncaught exception", exc_info=(exctype, value, tb))
    traceback_text = ''.join(traceback.format_exception(exctype, value, tb))
    QMessageBox.critical(None, "Error", f"An unexpected error occurred:\n\n{traceback_text}")

def setup_exception_handling():
    sys.excepthook = global_exception_handler
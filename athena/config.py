# athena/config.py

import os

# Application info
APP_NAME = "Athena AI Assistant"
APP_VERSION = "1.0.0"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_PATH = os.path.join(BASE_DIR, 'resources', 'icon.png')
DEFAULT_WORKSPACE = os.path.expanduser("~/Athena_Workspace")

# API Configuration
OLLAMA_BASE_URL = "http://localhost:11434"

# Logging
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'athena.log')
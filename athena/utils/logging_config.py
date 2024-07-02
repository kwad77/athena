# athena/utils/logging_config.py
import logging
import os
from athena.config import LOG_FILE

def setup_logging():
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=LOG_FILE,
        filemode='a'
    )

    # Also output to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    # Suppress overly verbose logs from libraries
    logging.getLogger('PyQt6').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
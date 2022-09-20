import logging
import os
import sys
import requests
from pathlib import Path

# Define paths
OUTPUT = Path("./output")
OUTPUT.mkdir(exist_ok=True)
LOG_PATH = OUTPUT / "out.log"
LOG_PATH.touch(exist_ok=True)

# Configure logging
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
term_handler = logging.StreamHandler(sys.stdout)
term_handler.setLevel(logging.INFO)
term_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
term_handler.setFormatter(term_format)
LOG.addHandler(term_handler)
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_format)
LOG.addHandler(file_handler)

LOG.debug("Test debug log record")
LOG.info("Test info log record")
LOG.warning("Test warning log record")
LOG.error("Test error log record.")

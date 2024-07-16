import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """Function to set up a logger with file and console handlers."""
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create file handler
    file_handler = RotatingFileHandler(os.path.join(log_dir, log_file), maxBytes=10485760, backupCount=5)  # 10MB file size
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a default logger for the application
app_logger = setup_logger('urbanpulse', 'app.log')

def get_logger(name: str):
    """Function to get a logger for a specific module."""
    return logging.getLogger(name)
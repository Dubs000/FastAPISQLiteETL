import logging
from app.logger import setup_logging, file_formatter
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Run the base setup
setup_logging()

# Creating a specific logger for the data loader
data_loader_logger = logging.getLogger('data_loader')
data_loader_logger.setLevel(logging.DEBUG)  # Setting a specific level for this logger

# Adding a file handler specifically for data loader logs
file_handler = logging.FileHandler(f'{base_dir}/logs/data_loader.log')
file_handler.setFormatter(file_formatter)
data_loader_logger.addHandler(file_handler)
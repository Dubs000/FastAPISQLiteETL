import logging
from app.logger import setup_logging, file_formatter
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Run the base setup
setup_logging()

# Creating a specific logger for the data loader
database_logger = logging.getLogger('database')
database_logger.setLevel(logging.DEBUG)  # Setting a specific level for this logger

# Adding a file handler specifically for data loader logs
file_handler = logging.FileHandler(f'{base_dir}/logs/database.log')
file_handler.setFormatter(file_formatter)
database_logger.addHandler(file_handler)
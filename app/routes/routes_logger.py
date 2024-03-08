import logging
from app.logger import setup_logging, file_formatter

setup_logging()

api_logger = logging.getLogger('api')
api_logger.setLevel(logging.INFO)  # Different level for API logs
api_file_handler = logging.FileHandler('logs/api.log')
api_file_handler.setFormatter(file_formatter)
api_logger.addHandler(api_file_handler)

# Use api_logger for logging within API-related modules
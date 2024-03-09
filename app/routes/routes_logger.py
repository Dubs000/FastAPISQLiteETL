import logging
from app.logger import setup_logging, file_formatter
import os

setup_logging()

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


api_logger = logging.getLogger('api')
api_logger.setLevel(logging.INFO)  # Different level for API logs
api_file_handler = logging.FileHandler(f'{base_dir}/logs/api.log')
api_file_handler.setFormatter(file_formatter)
api_logger.addHandler(api_file_handler)


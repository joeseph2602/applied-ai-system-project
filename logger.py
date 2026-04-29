import logging
import os

# Configure logging
LOG_FILE = os.path.join(os.path.dirname(__file__), 'pawpal.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_action(action: str):
    """Log a general action."""
    logging.info(action)

def log_error(error: str):
    """Log an error."""
    logging.error(error)

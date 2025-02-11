import logging
from config import LOG_FORMAT, LOG_LEVEL

def setup_logger():
    """Configure and return logger instance"""
    logger = logging.getLogger('CurrencyBot')
    logger.setLevel(LOG_LEVEL)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

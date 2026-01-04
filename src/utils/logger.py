import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, log_file: Path = None, level=logging.INFO):
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

# Create main project logger
project_logger = setup_logger(
    "tweet_sentiment",
    Path(__file__).parent.parent.parent / "logs" / f"{datetime.now().strftime('%Y%m%d')}.log"
)
import logging
import os
from pathlib import Path

def setup_logging():
    """Configure logging for the application"""
    # Create logs directory
    log_dir = Path.home() / "AppData" / "Roaming" / "Ace Centre" / "AACSpeakHelper" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Log file path
    log_file = log_dir / "config_manager.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Log startup
    logging.info("Starting AACSpeakHelper Config Manager")
    return log_file 
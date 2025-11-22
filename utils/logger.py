"""
Logging configuration module.
Provides centralized logging functionality for the framework.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config.config import Config


class Logger:
    """Custom logger class for the framework."""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str = __name__) -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name (typically __name__ of the module)
            
        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Avoid adding handlers multiple times
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                Config.LOG_FORMAT,
                datefmt=Config.LOG_DATE_FORMAT
            )
            console_handler.setFormatter(console_formatter)
            
            # File handler with rotation
            log_file = Config.get_log_path("automation")
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s",
                datefmt=Config.LOG_DATE_FORMAT
            )
            file_handler.setFormatter(file_formatter)
            
            # Add handlers
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
        
        cls._loggers[name] = logger
        return logger
    
    @classmethod
    def log_test_start(cls, test_name: str):
        """
        Log test start with separator.
        
        Args:
            test_name: Name of the test
        """
        logger = cls.get_logger()
        logger.info("=" * 80)
        logger.info(f"Starting Test: {test_name}")
        logger.info("=" * 80)
    
    @classmethod
    def log_test_end(cls, test_name: str, status: str):
        """
        Log test end with status.
        
        Args:
            test_name: Name of the test
            status: Test status (PASSED/FAILED)
        """
        logger = cls.get_logger()
        logger.info("=" * 80)
        logger.info(f"Test {test_name} - {status}")
        logger.info("=" * 80)
    
    @classmethod
    def log_step(cls, step_description: str):
        """
        Log a test step.
        
        Args:
            step_description: Description of the step
        """
        logger = cls.get_logger()
        logger.info(f"STEP: {step_description}")


# Convenience function
def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return Logger.get_logger(name)

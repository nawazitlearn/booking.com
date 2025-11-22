"""
Helper utilities module.
Provides common utility functions used across the framework.
"""

import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List
from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class DateHelper:
    """Helper class for date operations."""
    
    @staticmethod
    def get_future_date(days_from_now: int, date_format: str = "%Y-%m-%d") -> str:
        """
        Get a future date.
        
        Args:
            days_from_now: Number of days from today
            date_format: Date format string
            
        Returns:
            Formatted date string
        """
        future_date = datetime.now() + timedelta(days=days_from_now)
        return future_date.strftime(date_format)
    
    @staticmethod
    def get_date_range(start_days: int, end_days: int) -> tuple:
        """
        Get a date range.
        
        Args:
            start_days: Start date (days from now)
            end_days: End date (days from now)
            
        Returns:
            Tuple of (start_date, end_date) as strings
        """
        start_date = DateHelper.get_future_date(start_days)
        end_date = DateHelper.get_future_date(end_days)
        return start_date, end_date
    
    @staticmethod
    def format_date_for_booking(date_obj: datetime) -> str:
        """
        Format date for Booking.com.
        
        Args:
            date_obj: datetime object
            
        Returns:
            Formatted date string
        """
        return date_obj.strftime("%Y-%m-%d")


class DataHelper:
    """Helper class for data operations."""
    
    @staticmethod
    def load_test_data() -> Dict[str, Any]:
        """
        Load test data from JSON file.
        
        Returns:
            Dictionary containing test data
        """
        try:
            with open(Config.TEST_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Test data loaded successfully from {Config.TEST_DATA_FILE}")
            return data
        except Exception as e:
            logger.error(f"Failed to load test data: {e}")
            return {}
    
    @staticmethod
    def get_random_destination() -> str:
        """
        Get a random destination from test data.
        
        Returns:
            Random destination name
        """
        data = DataHelper.load_test_data()
        destinations = data.get("destinations", ["London"])
        return random.choice(destinations)
    
    @staticmethod
    def get_search_scenario(index: int = 0) -> Dict[str, Any]:
        """
        Get a search scenario from test data.
        
        Args:
            index: Index of the scenario (default: 0)
            
        Returns:
            Search scenario dictionary
        """
        data = DataHelper.load_test_data()
        scenarios = data.get("search_scenarios", [])
        if scenarios and 0 <= index < len(scenarios):
            return scenarios[index]
        return {}


class StringHelper:
    """Helper class for string operations."""
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """
        Generate a random string.
        
        Args:
            length: Length of the string
            
        Returns:
            Random string
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing extra whitespace.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        return ' '.join(text.split())
    
    @staticmethod
    def extract_number(text: str) -> float:
        """
        Extract number from text.
        
        Args:
            text: Text containing number
            
        Returns:
            Extracted number or 0.0 if not found
        """
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        return float(numbers[0]) if numbers else 0.0


class FileHelper:
    """Helper class for file operations."""
    
    @staticmethod
    def save_screenshot(driver, test_name: str) -> Path:
        """
        Save screenshot.
        
        Args:
            driver: WebDriver instance
            test_name: Name of the test
            
        Returns:
            Path to saved screenshot
        """
        screenshot_path = Config.get_screenshot_path(test_name)
        try:
            driver.save_screenshot(str(screenshot_path))
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            return None
    
    @staticmethod
    def ensure_directory_exists(directory: Path):
        """
        Ensure directory exists.
        
        Args:
            directory: Directory path
        """
        directory.mkdir(parents=True, exist_ok=True)


class WaitHelper:
    """Helper class for wait operations."""
    
    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 10, poll_frequency: float = 0.5) -> bool:
        """
        Wait for a condition to be true.
        
        Args:
            condition_func: Function that returns boolean
            timeout: Maximum wait time in seconds
            poll_frequency: How often to check condition
            
        Returns:
            True if condition met, False otherwise
        """
        import time
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                if condition_func():
                    return True
            except Exception:
                pass
            time.sleep(poll_frequency)
        return False

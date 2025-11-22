"""
Configuration module for the automation framework.
Manages all configuration settings including URLs, timeouts, browser settings, etc.
"""

import os
from pathlib import Path


class Config:
    """Central configuration class for the framework."""
    
    # Base URL
    BASE_URL = "https://www.booking.com/index.en-gb.html"
    
    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome").lower()  # chrome, firefox, edge
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    
    # Timeout settings (in seconds)
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    
    # Window settings
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    MAXIMIZE_WINDOW = True
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    REPORTS_DIR = PROJECT_ROOT / "reports"
    LOGS_DIR = PROJECT_ROOT / "logs"
    SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
    TEST_DATA_FILE = PROJECT_ROOT / "config" / "test_data.json"
    
    # Ensure directories exist
    REPORTS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE = True
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Browser options
    CHROME_OPTIONS = [
        "--disable-notifications",
        "--disable-popup-blocking",
        "--disable-infobars",
        "--disable-extensions",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]
    
    FIREFOX_OPTIONS = [
        "--disable-notifications",
    ]
    
    EDGE_OPTIONS = [
        "--disable-notifications",
        "--disable-popup-blocking",
    ]
    
    @classmethod
    def get_browser_options(cls, browser: str = None) -> list:
        """
        Get browser-specific options.
        
        Args:
            browser: Browser name (chrome, firefox, edge)
            
        Returns:
            List of browser options
        """
        browser = browser or cls.BROWSER
        
        if browser == "chrome":
            return cls.CHROME_OPTIONS.copy()
        elif browser == "firefox":
            return cls.FIREFOX_OPTIONS.copy()
        elif browser == "edge":
            return cls.EDGE_OPTIONS.copy()
        else:
            return []
    
    @classmethod
    def get_screenshot_path(cls, test_name: str) -> Path:
        """
        Generate screenshot path for a test.
        
        Args:
            test_name: Name of the test
            
        Returns:
            Path object for screenshot
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        return cls.SCREENSHOTS_DIR / filename
    
    @classmethod
    def get_log_path(cls, log_name: str = "automation") -> Path:
        """
        Generate log file path.
        
        Args:
            log_name: Name of the log file
            
        Returns:
            Path object for log file
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"{log_name}_{timestamp}.log"
        return cls.LOGS_DIR / filename

"""
WebDriver factory module.
Manages WebDriver creation and configuration for different browsers.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class DriverFactory:
    """Factory class for creating WebDriver instances."""
    
    @staticmethod
    def create_driver(browser: str = None, headless: bool = None):
        """
        Create and configure a WebDriver instance.
        
        Args:
            browser: Browser name (chrome, firefox, edge). Uses Config.BROWSER if not provided.
            headless: Run in headless mode. Uses Config.HEADLESS if not provided.
            
        Returns:
            Configured WebDriver instance
            
        Raises:
            ValueError: If browser is not supported
        """
        browser = browser or Config.BROWSER
        headless = headless if headless is not None else Config.HEADLESS
        
        logger.info(f"Creating {browser} driver (headless: {headless})")
        
        if browser.lower() == "chrome":
            driver = DriverFactory._create_chrome_driver(headless)
        elif browser.lower() == "firefox":
            driver = DriverFactory._create_firefox_driver(headless)
        elif browser.lower() == "edge":
            driver = DriverFactory._create_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Configure driver
        DriverFactory._configure_driver(driver)
        
        logger.info(f"{browser} driver created successfully")
        return driver
    
    @staticmethod
    def _create_chrome_driver(headless: bool):
        """Create Chrome driver using Selenium Manager (Selenium 4.6+)."""
        options = webdriver.ChromeOptions()
        
        # Add options
        for option in Config.get_browser_options("chrome"):
            options.add_argument(option)
        
        if headless:
            options.add_argument("--headless=new")
        
        # Additional Chrome-specific options
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        })
        
        # Use Selenium Manager (built-in to Selenium 4.6+)
        # This automatically downloads and manages the correct driver
        try:
            driver = webdriver.Chrome(options=options)
            logger.info("ChromeDriver created successfully using Selenium Manager")
        except Exception as e:
            logger.warning(f"Selenium Manager failed: {e}, trying webdriver-manager")
            # Fallback to webdriver-manager
            try:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e2:
                logger.error(f"Both Selenium Manager and webdriver-manager failed: {e2}")
                raise
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless: bool):
        """Create Firefox driver."""
        options = webdriver.FirefoxOptions()
        
        # Add options
        for option in Config.get_browser_options("firefox"):
            options.add_argument(option)
        
        if headless:
            options.add_argument("--headless")
        
        # Additional Firefox-specific options
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("dom.push.enabled", False)
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        return driver
    
    @staticmethod
    def _create_edge_driver(headless: bool):
        """Create Edge driver."""
        options = webdriver.EdgeOptions()
        
        # Add options
        for option in Config.get_browser_options("edge"):
            options.add_argument(option)
        
        if headless:
            options.add_argument("--headless=new")
        
        # Additional Edge-specific options
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        return driver
    
    @staticmethod
    def _configure_driver(driver):
        """
        Configure driver with common settings.
        
        Args:
            driver: WebDriver instance
        """
        # Set timeouts
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        # Set window size
        if Config.MAXIMIZE_WINDOW:
            driver.maximize_window()
        else:
            driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        
        logger.info("Driver configured with timeouts and window settings")
    
    @staticmethod
    def quit_driver(driver):
        """
        Safely quit the driver.
        
        Args:
            driver: WebDriver instance
        """
        try:
            if driver:
                driver.quit()
                logger.info("Driver quit successfully")
        except Exception as e:
            logger.error(f"Error quitting driver: {e}")

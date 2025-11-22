"""
Base Page module.
Contains the BasePage class with common methods for all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from config.config import Config
from utils.logger import get_logger
from utils.decorators import log_action, retry
import allure

logger = get_logger(__name__)


class BasePage:
    """Base page class with common methods for all page objects."""
    
    def __init__(self, driver):
        """
        Initialize BasePage.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
    
    @log_action
    def open_url(self, url: str):
        """
        Open a URL.
        
        Args:
            url: URL to open
        """
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)
        allure.attach(url, name="URL", attachment_type=allure.attachment_type.TEXT)
    
    @retry(max_attempts=3, delay=1.0, exceptions=(StaleElementReferenceException,))
    def find_element(self, locator: tuple, timeout: int = None):
        """
        Find an element with explicit wait.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Custom timeout (uses Config.EXPLICIT_WAIT if not provided)
            
        Returns:
            WebElement
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    @retry(max_attempts=3, delay=1.0, exceptions=(StaleElementReferenceException,))
    def find_elements(self, locator: tuple, timeout: int = None):
        """
        Find multiple elements.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Custom timeout
            
        Returns:
            List of WebElements
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            logger.warning(f"Elements not found: {locator}")
            return []
    
    @log_action
    def click(self, locator: tuple, timeout: int = None):
        """
        Click an element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Custom timeout
        """
        try:
            element = self.wait_for_clickable(locator, timeout)
            element.click()
            logger.info(f"Clicked element: {locator}")
        except ElementClickInterceptedException:
            logger.warning(f"Click intercepted, trying JavaScript click: {locator}")
            self.click_with_js(locator)
    
    @log_action
    def click_with_js(self, locator: tuple):
        """
        Click element using JavaScript.
        
        Args:
            locator: Tuple of (By, value)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        logger.info(f"Clicked element with JS: {locator}")
    
    @log_action
    def type_text(self, locator: tuple, text: str, clear_first: bool = True):
        """
        Type text into an element.
        
        Args:
            locator: Tuple of (By, value)
            text: Text to type
            clear_first: Clear field before typing
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Typed '{text}' into element: {locator}")
    
    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Custom timeout
            
        Returns:
            Element text
        """
        element = self.find_element(locator, timeout)
        text = element.text
        logger.info(f"Got text '{text}' from element: {locator}")
        return text
    
    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        Get attribute value from an element.
        
        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        return value
    
    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Custom timeout
            
        Returns:
            True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Check if element is present in DOM.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Custom timeout
            
        Returns:
            True if present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_clickable(self, locator: tuple, timeout: int = None):
        """
        Wait for element to be clickable.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Custom timeout
            
        Returns:
            WebElement
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    
    def wait_for_invisibility(self, locator: tuple, timeout: int = None) -> bool:
        """
        Wait for element to become invisible.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Custom timeout
            
        Returns:
            True if invisible, False otherwise
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @log_action
    def scroll_to_element(self, locator: tuple):
        """
        Scroll to an element.
        
        Args:
            locator: Tuple of (By, value)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.info(f"Scrolled to element: {locator}")
    
    @log_action
    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    @log_action
    def scroll_to_top(self):
        """Scroll to top of page."""
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def execute_script(self, script: str, *args):
        """
        Execute JavaScript.
        
        Args:
            script: JavaScript code
            *args: Arguments to pass to script
            
        Returns:
            Script result
        """
        return self.driver.execute_script(script, *args)
    
    def get_current_url(self) -> str:
        """
        Get current URL.
        
        Returns:
            Current URL
        """
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """
        Get page title.
        
        Returns:
            Page title
        """
        return self.driver.title
    
    @log_action
    def switch_to_frame(self, locator: tuple):
        """
        Switch to iframe.
        
        Args:
            locator: Tuple of (By, value)
        """
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
    
    @log_action
    def switch_to_default_content(self):
        """Switch back to default content."""
        self.driver.switch_to.default_content()
    
    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Take a screenshot.
        
        Args:
            name: Screenshot name
            
        Returns:
            Screenshot path
        """
        from utils.helpers import FileHelper
        screenshot_path = FileHelper.save_screenshot(self.driver, name)
        return str(screenshot_path)
    
    @log_action
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
    
    def wait_for_page_load(self, timeout: int = None):
        """
        Wait for page to load completely.
        
        Args:
            timeout: Custom timeout
        """
        timeout = timeout or Config.PAGE_LOAD_TIMEOUT
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        logger.info("Page loaded completely")

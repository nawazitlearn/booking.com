"""
Home Page module.
Contains page object for Booking.com homepage.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from config.config import Config
from utils.logger import get_logger
from utils.decorators import allure_step
import allure
import time

logger = get_logger(__name__)


class HomePage(BasePage):
    """Page object for Booking.com homepage."""
    
    # Locators
    COOKIE_ACCEPT_BUTTON = (By.ID, "onetrust-accept-btn-handler")
    COOKIE_BANNER = (By.ID, "onetrust-banner-sdk")
    DESTINATION_INPUT = (By.CSS_SELECTOR, "input[name='ss']")
    DESTINATION_INPUT_ALT = (By.CSS_SELECTOR, "input[placeholder*='Where are you going']")
    DATE_PICKER = (By.CSS_SELECTOR, "div[data-testid='searchbox-dates-container']")
    CHECK_IN_DATE = (By.CSS_SELECTOR, "span[data-date='{}']")
    CHECK_OUT_DATE = (By.CSS_SELECTOR, "span[data-date='{}']")
    CALENDAR_NEXT_BUTTON = (By.CSS_SELECTOR, "button[aria-label*='Next month']")
    GUESTS_BUTTON = (By.CSS_SELECTOR, "button[data-testid='occupancy-config']")
    ADULTS_DECREASE = (By.CSS_SELECTOR, "button[aria-label*='Decrease number of Adults']")
    ADULTS_INCREASE = (By.CSS_SELECTOR, "button[aria-label*='Increase number of Adults']")
    CHILDREN_DECREASE = (By.CSS_SELECTOR, "button[aria-label*='Decrease number of Children']")
    CHILDREN_INCREASE = (By.CSS_SELECTOR, "button[aria-label*='Increase number of Children']")
    ROOMS_DECREASE = (By.CSS_SELECTOR, "button[aria-label*='Decrease number of Rooms']")
    ROOMS_INCREASE = (By.CSS_SELECTOR, "button[aria-label*='Increase number of Rooms']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SEARCH_BUTTON_ALT = (By.CSS_SELECTOR, "button span.e4adce92df")
    
    def __init__(self, driver):
        """
        Initialize HomePage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
    
    @allure_step("Open Booking.com homepage")
    def open(self):
        """Open the homepage."""
        self.open_url(Config.BASE_URL)
        self.wait_for_page_load()
        time.sleep(2)  # Allow page to settle
        self.close_cookie_banner()
    
    @allure_step("Close cookie consent banner")
    def close_cookie_banner(self):
        """Close cookie consent banner if present."""
        try:
            if self.is_element_visible(self.COOKIE_BANNER, timeout=5):
                logger.info("Cookie banner detected, attempting to close")
                self.click(self.COOKIE_ACCEPT_BUTTON, timeout=5)
                self.wait_for_invisibility(self.COOKIE_BANNER, timeout=5)
                logger.info("Cookie banner closed")
                time.sleep(1)
        except Exception as e:
            logger.warning(f"Could not close cookie banner: {e}")
    
    @allure_step("Enter destination: {destination}")
    def enter_destination(self, destination: str):
        """
        Enter destination in search box.
        
        Args:
            destination: Destination name
        """
        try:
            # Try primary locator
            if self.is_element_visible(self.DESTINATION_INPUT, timeout=5):
                self.click(self.DESTINATION_INPUT)
                self.type_text(self.DESTINATION_INPUT, destination)
            else:
                # Try alternative locator
                self.click(self.DESTINATION_INPUT_ALT)
                self.type_text(self.DESTINATION_INPUT_ALT, destination)
            
            time.sleep(2)  # Wait for autocomplete
            
            # Press Enter or Down+Enter to select first suggestion
            element = self.find_element(self.DESTINATION_INPUT) if self.is_element_present(self.DESTINATION_INPUT) else self.find_element(self.DESTINATION_INPUT_ALT)
            element.send_keys(Keys.ARROW_DOWN)
            element.send_keys(Keys.ENTER)
            
            logger.info(f"Entered destination: {destination}")
            allure.attach(destination, name="Destination", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            logger.error(f"Failed to enter destination: {e}")
            raise
    
    @allure_step("Select check-in date: {check_in_date}")
    def select_check_in_date(self, check_in_date: str):
        """
        Select check-in date.
        
        Args:
            check_in_date: Date in format YYYY-MM-DD
        """
        try:
            # Open date picker if not already open
            if not self.is_element_visible((By.CSS_SELECTOR, "div[data-testid='searchbox-datepicker-calendar']"), timeout=3):
                self.click(self.DATE_PICKER)
                time.sleep(1)
            
            # Navigate to correct month if needed and select date
            self._select_date(check_in_date)
            logger.info(f"Selected check-in date: {check_in_date}")
            allure.attach(check_in_date, name="Check-in Date", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            logger.error(f"Failed to select check-in date: {e}")
            raise
    
    @allure_step("Select check-out date: {check_out_date}")
    def select_check_out_date(self, check_out_date: str):
        """
        Select check-out date.
        
        Args:
            check_out_date: Date in format YYYY-MM-DD
        """
        try:
            self._select_date(check_out_date)
            logger.info(f"Selected check-out date: {check_out_date}")
            allure.attach(check_out_date, name="Check-out Date", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            logger.error(f"Failed to select check-out date: {e}")
            raise
    
    def _select_date(self, date: str):
        """
        Internal method to select a date from calendar.
        
        Args:
            date: Date in format YYYY-MM-DD
        """
        date_locator = (By.CSS_SELECTOR, f"span[data-date='{date}']")
        
        # Try to find and click the date (may need to navigate months)
        max_attempts = 12  # Maximum 12 months to search
        for _ in range(max_attempts):
            if self.is_element_visible(date_locator, timeout=2):
                self.click(date_locator)
                return
            else:
                # Click next month button
                try:
                    self.click(self.CALENDAR_NEXT_BUTTON, timeout=2)
                    time.sleep(0.5)
                except:
                    break
        
        raise Exception(f"Could not find date: {date}")
    
    @allure_step("Configure guests - Adults: {adults}, Children: {children}, Rooms: {rooms}")
    def select_guests(self, adults: int = 2, children: int = 0, rooms: int = 1):
        """
        Configure number of guests and rooms.
        
        Args:
            adults: Number of adults
            children: Number of children
            rooms: Number of rooms
        """
        try:
            # Open guests selector
            self.click(self.GUESTS_BUTTON)
            time.sleep(1)
            
            # Set adults (default is usually 2, so adjust accordingly)
            self._adjust_counter(self.ADULTS_DECREASE, self.ADULTS_INCREASE, adults, default=2)
            
            # Set children (default is usually 0)
            self._adjust_counter(self.CHILDREN_DECREASE, self.CHILDREN_INCREASE, children, default=0)
            
            # Set rooms (default is usually 1)
            self._adjust_counter(self.ROOMS_DECREASE, self.ROOMS_INCREASE, rooms, default=1)
            
            logger.info(f"Configured guests: {adults} adults, {children} children, {rooms} rooms")
            allure.attach(
                f"Adults: {adults}, Children: {children}, Rooms: {rooms}",
                name="Guest Configuration",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Close the guests selector (click outside or on a specific close button)
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Failed to configure guests: {e}")
            raise
    
    def _adjust_counter(self, decrease_locator: tuple, increase_locator: tuple, target: int, default: int = 0):
        """
        Adjust a counter (adults/children/rooms) to target value.
        
        Args:
            decrease_locator: Locator for decrease button
            increase_locator: Locator for increase button
            target: Target value
            default: Default value
        """
        current = default
        
        while current < target:
            self.click(increase_locator)
            current += 1
            time.sleep(0.3)
        
        while current > target:
            self.click(decrease_locator)
            current -= 1
            time.sleep(0.3)
    
    @allure_step("Click search button")
    def click_search(self):
        """Click the search button."""
        try:
            # Try primary search button
            if self.is_element_visible(self.SEARCH_BUTTON, timeout=5):
                self.click(self.SEARCH_BUTTON)
            else:
                # Try alternative search button
                self.click(self.SEARCH_BUTTON_ALT)
            
            logger.info("Clicked search button")
            time.sleep(2)  # Wait for search results to load
        except Exception as e:
            logger.error(f"Failed to click search button: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """
        Check if homepage is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return self.is_element_visible(self.DESTINATION_INPUT, timeout=10) or \
               self.is_element_visible(self.DESTINATION_INPUT_ALT, timeout=10)
    
    @allure_step("Perform search - Destination: {destination}")
    def search(self, destination: str, check_in_date: str = None, check_out_date: str = None, 
               adults: int = 2, children: int = 0, rooms: int = 1):
        """
        Perform a complete search.
        
        Args:
            destination: Destination name
            check_in_date: Check-in date (YYYY-MM-DD)
            check_out_date: Check-out date (YYYY-MM-DD)
            adults: Number of adults
            children: Number of children
            rooms: Number of rooms
        """
        self.enter_destination(destination)
        
        if check_in_date and check_out_date:
            self.select_check_in_date(check_in_date)
            self.select_check_out_date(check_out_date)
        
        self.select_guests(adults, children, rooms)
        self.click_search()

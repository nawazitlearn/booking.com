"""
Search Results Page module.
Contains page object for Booking.com search results page.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.decorators import allure_step
import allure
import time

logger = get_logger(__name__)


class SearchResultsPage(BasePage):
    """Page object for Booking.com search results page."""
    
    # Locators
    SEARCH_RESULTS_CONTAINER = (By.CSS_SELECTOR, "div[data-testid='property-card']")
    PROPERTY_CARDS = (By.CSS_SELECTOR, "div[data-testid='property-card']")
    PROPERTY_TITLES = (By.CSS_SELECTOR, "div[data-testid='title']")
    PROPERTY_PRICES = (By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']")
    FIRST_PROPERTY = (By.CSS_SELECTOR, "div[data-testid='property-card']:first-of-type")
    FIRST_PROPERTY_TITLE = (By.CSS_SELECTOR, "div[data-testid='property-card']:first-of-type div[data-testid='title']")
    
    # Filter locators
    PRICE_FILTER_MIN = (By.CSS_SELECTOR, "input[name='price_filter_min']")
    PRICE_FILTER_MAX = (By.CSS_SELECTOR, "input[name='price_filter_max']")
    STAR_RATING_FILTER = (By.CSS_SELECTOR, "div[data-filters-group='class'] input[value='{}']")
    FILTER_BUTTON = (By.CSS_SELECTOR, "button[data-testid='filter-button']")
    
    # Sort locators
    SORT_DROPDOWN = (By.CSS_SELECTOR, "button[data-testid='sorters-dropdown-trigger']")
    SORT_OPTION = (By.CSS_SELECTOR, "button[data-id='{}']")
    
    # Results info
    RESULTS_COUNT = (By.CSS_SELECTOR, "h1")
    LOADING_INDICATOR = (By.CSS_SELECTOR, "div[data-testid='overlay-spinner']")
    
    def __init__(self, driver):
        """
        Initialize SearchResultsPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
    
    def is_loaded(self) -> bool:
        """
        Check if search results page is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return self.is_element_visible(self.SEARCH_RESULTS_CONTAINER, timeout=15)
    
    def wait_for_results_to_load(self):
        """Wait for search results to load completely."""
        # Wait for loading indicator to disappear
        self.wait_for_invisibility(self.LOADING_INDICATOR, timeout=20)
        # Wait for property cards to be visible
        self.is_element_visible(self.PROPERTY_CARDS, timeout=15)
        time.sleep(2)  # Additional wait for dynamic content
        logger.info("Search results loaded")
    
    @allure_step("Get search results count")
    def get_search_results_count(self) -> int:
        """
        Get the number of search results.
        
        Returns:
            Number of property cards found
        """
        try:
            self.wait_for_results_to_load()
            properties = self.find_elements(self.PROPERTY_CARDS, timeout=10)
            count = len(properties)
            logger.info(f"Found {count} properties")
            allure.attach(str(count), name="Results Count", attachment_type=allure.attachment_type.TEXT)
            return count
        except Exception as e:
            logger.error(f"Failed to get results count: {e}")
            return 0
    
    @allure_step("Get first hotel name")
    def get_first_hotel_name(self) -> str:
        """
        Get the name of the first hotel in results.
        
        Returns:
            Hotel name
        """
        try:
            self.wait_for_results_to_load()
            hotel_name = self.get_text(self.FIRST_PROPERTY_TITLE, timeout=10)
            logger.info(f"First hotel: {hotel_name}")
            allure.attach(hotel_name, name="First Hotel", attachment_type=allure.attachment_type.TEXT)
            return hotel_name
        except Exception as e:
            logger.error(f"Failed to get first hotel name: {e}")
            return ""
    
    @allure_step("Click first hotel")
    def click_first_hotel(self):
        """Click on the first hotel in search results."""
        try:
            self.wait_for_results_to_load()
            
            # Store the original window handle
            original_window = self.driver.current_window_handle
            
            # Click the first property
            self.scroll_to_element(self.FIRST_PROPERTY_TITLE)
            time.sleep(1)
            self.click(self.FIRST_PROPERTY_TITLE)
            
            # Wait for new window/tab to open
            time.sleep(3)
            
            # Switch to new window if opened
            windows = self.driver.window_handles
            if len(windows) > 1:
                for window in windows:
                    if window != original_window:
                        self.driver.switch_to.window(window)
                        logger.info("Switched to hotel details window")
                        break
            
            logger.info("Clicked first hotel")
        except Exception as e:
            logger.error(f"Failed to click first hotel: {e}")
            raise
    
    @allure_step("Apply price filter - Min: {min_price}, Max: {max_price}")
    def apply_price_filter(self, min_price: int = None, max_price: int = None):
        """
        Apply price filter.
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
        """
        try:
            if min_price:
                if self.is_element_visible(self.PRICE_FILTER_MIN, timeout=5):
                    self.type_text(self.PRICE_FILTER_MIN, str(min_price))
                    logger.info(f"Set minimum price: {min_price}")
            
            if max_price:
                if self.is_element_visible(self.PRICE_FILTER_MAX, timeout=5):
                    self.type_text(self.PRICE_FILTER_MAX, str(max_price))
                    logger.info(f"Set maximum price: {max_price}")
            
            time.sleep(2)
            self.wait_for_results_to_load()
            
            allure.attach(
                f"Min: {min_price}, Max: {max_price}",
                name="Price Filter",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as e:
            logger.warning(f"Could not apply price filter: {e}")
    
    @allure_step("Apply star rating filter: {rating}")
    def apply_rating_filter(self, rating: int):
        """
        Apply star rating filter.
        
        Args:
            rating: Star rating (1-5)
        """
        try:
            rating_locator = (By.CSS_SELECTOR, f"div[data-filters-group='class'] input[value='{rating}']")
            
            if self.is_element_visible(rating_locator, timeout=5):
                # Scroll to filter section
                self.scroll_to_element(rating_locator)
                time.sleep(0.5)
                
                # Click the rating filter
                self.click_with_js(rating_locator)
                logger.info(f"Applied {rating}-star rating filter")
                
                time.sleep(2)
                self.wait_for_results_to_load()
                
                allure.attach(str(rating), name="Star Rating", attachment_type=allure.attachment_type.TEXT)
            else:
                logger.warning(f"Rating filter {rating} not found")
        except Exception as e:
            logger.warning(f"Could not apply rating filter: {e}")
    
    @allure_step("Sort by: {sort_option}")
    def sort_by(self, sort_option: str):
        """
        Sort search results.
        
        Args:
            sort_option: Sort option (e.g., 'price', 'review_score_and_price', 'distance')
        """
        try:
            # Open sort dropdown
            if self.is_element_visible(self.SORT_DROPDOWN, timeout=5):
                self.click(self.SORT_DROPDOWN)
                time.sleep(1)
                
                # Select sort option
                sort_locator = (By.CSS_SELECTOR, f"button[data-id='{sort_option}']")
                if self.is_element_visible(sort_locator, timeout=5):
                    self.click(sort_locator)
                    logger.info(f"Sorted by: {sort_option}")
                    
                    time.sleep(2)
                    self.wait_for_results_to_load()
                    
                    allure.attach(sort_option, name="Sort Option", attachment_type=allure.attachment_type.TEXT)
                else:
                    logger.warning(f"Sort option {sort_option} not found")
            else:
                logger.warning("Sort dropdown not found")
        except Exception as e:
            logger.warning(f"Could not apply sort: {e}")
    
    def get_all_property_names(self) -> list:
        """
        Get names of all properties on current page.
        
        Returns:
            List of property names
        """
        try:
            self.wait_for_results_to_load()
            title_elements = self.find_elements(self.PROPERTY_TITLES, timeout=10)
            names = [element.text for element in title_elements if element.text]
            logger.info(f"Retrieved {len(names)} property names")
            return names
        except Exception as e:
            logger.error(f"Failed to get property names: {e}")
            return []
    
    def get_all_property_prices(self) -> list:
        """
        Get prices of all properties on current page.
        
        Returns:
            List of property prices as strings
        """
        try:
            self.wait_for_results_to_load()
            price_elements = self.find_elements(self.PROPERTY_PRICES, timeout=10)
            prices = [element.text for element in price_elements if element.text]
            logger.info(f"Retrieved {len(prices)} property prices")
            return prices
        except Exception as e:
            logger.error(f"Failed to get property prices: {e}")
            return []
    
    @allure_step("Verify filters are applied")
    def verify_filters_applied(self) -> bool:
        """
        Verify that filters are applied (results changed).
        
        Returns:
            True if filters appear to be applied
        """
        try:
            # Check if we have results
            count = self.get_search_results_count()
            return count > 0
        except Exception as e:
            logger.error(f"Failed to verify filters: {e}")
            return False

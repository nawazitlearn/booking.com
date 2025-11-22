"""
Hotel Details Page module.
Contains page object for Booking.com hotel details page.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.decorators import allure_step
import allure
import time

logger = get_logger(__name__)


class HotelDetailsPage(BasePage):
    """Page object for Booking.com hotel details page."""
    
    # Locators
    HOTEL_NAME = (By.CSS_SELECTOR, "h2[data-testid='property-name']")
    HOTEL_NAME_ALT = (By.CSS_SELECTOR, "h2.pp-header__title")
    HOTEL_RATING = (By.CSS_SELECTOR, "div[data-testid='rating-stars']")
    HOTEL_RATING_ALT = (By.CSS_SELECTOR, "span[data-testid='rating-score']")
    HOTEL_PRICE = (By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']")
    HOTEL_PRICE_ALT = (By.CSS_SELECTOR, "div.prco-valign-middle-helper")
    AMENITIES_SECTION = (By.CSS_SELECTOR, "div[data-testid='property-most-popular-facilities']")
    AMENITIES_LIST = (By.CSS_SELECTOR, "div[data-testid='property-most-popular-facilities'] span")
    AVAILABILITY_BUTTON = (By.CSS_SELECTOR, "button[data-testid='availability-cta']")
    AVAILABILITY_BUTTON_ALT = (By.CSS_SELECTOR, "a.bui-button--primary")
    PHOTOS_SECTION = (By.CSS_SELECTOR, "div[data-testid='property-gallery']")
    DESCRIPTION = (By.CSS_SELECTOR, "div[data-testid='property-description']")
    
    def __init__(self, driver):
        """
        Initialize HotelDetailsPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
    
    def is_loaded(self) -> bool:
        """
        Check if hotel details page is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return self.is_element_visible(self.HOTEL_NAME, timeout=15) or \
               self.is_element_visible(self.HOTEL_NAME_ALT, timeout=15)
    
    def wait_for_page_to_load(self):
        """Wait for hotel details page to load completely."""
        self.wait_for_page_load()
        time.sleep(2)  # Additional wait for dynamic content
        logger.info("Hotel details page loaded")
    
    @allure_step("Get hotel name")
    def get_hotel_name(self) -> str:
        """
        Get hotel name.
        
        Returns:
            Hotel name
        """
        try:
            self.wait_for_page_to_load()
            
            # Try primary locator
            if self.is_element_visible(self.HOTEL_NAME, timeout=5):
                name = self.get_text(self.HOTEL_NAME)
            else:
                # Try alternative locator
                name = self.get_text(self.HOTEL_NAME_ALT)
            
            logger.info(f"Hotel name: {name}")
            allure.attach(name, name="Hotel Name", attachment_type=allure.attachment_type.TEXT)
            return name
        except Exception as e:
            logger.error(f"Failed to get hotel name: {e}")
            return ""
    
    @allure_step("Get hotel rating")
    def get_hotel_rating(self) -> str:
        """
        Get hotel star rating.
        
        Returns:
            Hotel rating
        """
        try:
            # Try to get star rating
            if self.is_element_visible(self.HOTEL_RATING, timeout=5):
                rating_element = self.find_element(self.HOTEL_RATING)
                # Get aria-label or count stars
                rating = rating_element.get_attribute("aria-label")
                logger.info(f"Hotel rating: {rating}")
                allure.attach(rating, name="Hotel Rating", attachment_type=allure.attachment_type.TEXT)
                return rating
            elif self.is_element_visible(self.HOTEL_RATING_ALT, timeout=5):
                rating = self.get_text(self.HOTEL_RATING_ALT)
                logger.info(f"Hotel rating: {rating}")
                allure.attach(rating, name="Hotel Rating", attachment_type=allure.attachment_type.TEXT)
                return rating
            else:
                logger.warning("Rating not found")
                return "N/A"
        except Exception as e:
            logger.error(f"Failed to get hotel rating: {e}")
            return "N/A"
    
    @allure_step("Get hotel price")
    def get_hotel_price(self) -> str:
        """
        Get hotel price.
        
        Returns:
            Hotel price
        """
        try:
            # Try primary locator
            if self.is_element_visible(self.HOTEL_PRICE, timeout=5):
                price = self.get_text(self.HOTEL_PRICE)
            else:
                # Try alternative locator
                price = self.get_text(self.HOTEL_PRICE_ALT)
            
            logger.info(f"Hotel price: {price}")
            allure.attach(price, name="Hotel Price", attachment_type=allure.attachment_type.TEXT)
            return price
        except Exception as e:
            logger.warning(f"Could not get hotel price: {e}")
            return "N/A"
    
    @allure_step("Get hotel amenities")
    def get_amenities(self) -> list:
        """
        Get list of hotel amenities.
        
        Returns:
            List of amenities
        """
        try:
            if self.is_element_visible(self.AMENITIES_SECTION, timeout=5):
                self.scroll_to_element(self.AMENITIES_SECTION)
                time.sleep(1)
                
                amenity_elements = self.find_elements(self.AMENITIES_LIST, timeout=5)
                amenities = [element.text for element in amenity_elements if element.text]
                
                logger.info(f"Found {len(amenities)} amenities")
                allure.attach(
                    "\n".join(amenities),
                    name="Amenities",
                    attachment_type=allure.attachment_type.TEXT
                )
                return amenities
            else:
                logger.warning("Amenities section not found")
                return []
        except Exception as e:
            logger.error(f"Failed to get amenities: {e}")
            return []
    
    @allure_step("Check availability")
    def check_availability(self):
        """Click the check availability button."""
        try:
            # Scroll to availability button
            if self.is_element_visible(self.AVAILABILITY_BUTTON, timeout=5):
                self.scroll_to_element(self.AVAILABILITY_BUTTON)
                time.sleep(1)
                self.click(self.AVAILABILITY_BUTTON)
            elif self.is_element_visible(self.AVAILABILITY_BUTTON_ALT, timeout=5):
                self.scroll_to_element(self.AVAILABILITY_BUTTON_ALT)
                time.sleep(1)
                self.click(self.AVAILABILITY_BUTTON_ALT)
            else:
                logger.warning("Availability button not found")
                return
            
            logger.info("Clicked availability button")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Failed to check availability: {e}")
            raise
    
    @allure_step("Verify hotel details are loaded")
    def verify_hotel_details_loaded(self) -> bool:
        """
        Verify that hotel details page is properly loaded with key information.
        
        Returns:
            True if details are loaded, False otherwise
        """
        try:
            # Check for hotel name
            has_name = self.is_element_visible(self.HOTEL_NAME, timeout=10) or \
                       self.is_element_visible(self.HOTEL_NAME_ALT, timeout=10)
            
            if not has_name:
                logger.error("Hotel name not found")
                return False
            
            # Check for photos section
            has_photos = self.is_element_visible(self.PHOTOS_SECTION, timeout=5)
            
            logger.info(f"Hotel details loaded - Name: {has_name}, Photos: {has_photos}")
            return has_name
        except Exception as e:
            logger.error(f"Failed to verify hotel details: {e}")
            return False
    
    def get_hotel_description(self) -> str:
        """
        Get hotel description.
        
        Returns:
            Hotel description text
        """
        try:
            if self.is_element_visible(self.DESCRIPTION, timeout=5):
                self.scroll_to_element(self.DESCRIPTION)
                description = self.get_text(self.DESCRIPTION)
                logger.info("Retrieved hotel description")
                return description
            else:
                logger.warning("Description not found")
                return ""
        except Exception as e:
            logger.error(f"Failed to get description: {e}")
            return ""

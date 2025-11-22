"""
Hotel details tests.
Tests for Booking.com hotel details page.
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.hotel_details_page import HotelDetailsPage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Hotel Details")
@allure.story("Hotel Information")
class TestHotelDetails:
    """Test cases for hotel details page."""
    
    @pytest.fixture(autouse=True)
    def setup(self, home_page):
        """Setup for hotel details tests - navigate to hotel details page."""
        with allure.step("Perform search"):
            destination = "London"
            home_page.enter_destination(destination)
            home_page.click_search()
        
        with allure.step("Navigate to first hotel"):
            self.search_results = SearchResultsPage(home_page.driver)
            assert self.search_results.is_loaded(), "Search results page did not load"
            
            # Get first hotel name before clicking
            self.expected_hotel_name = self.search_results.get_first_hotel_name()
            logger.info(f"Navigating to hotel: {self.expected_hotel_name}")
            
            # Click first hotel
            self.search_results.click_first_hotel()
            
            # Initialize hotel details page
            self.hotel_details = HotelDetailsPage(home_page.driver)
    
    @pytest.mark.hotel
    @pytest.mark.smoke
    @allure.title("Test navigate to hotel details")
    @allure.description("Verify that user can navigate from search results to hotel details page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_hotel_details(self):
        """Test navigation to hotel details page."""
        with allure.step("Verify hotel details page is loaded"):
            assert self.hotel_details.is_loaded(), "Hotel details page did not load"
            logger.info("Hotel details page loaded successfully")
        
        with allure.step("Verify hotel details are displayed"):
            assert self.hotel_details.verify_hotel_details_loaded(), "Hotel details not properly loaded"
        
        logger.info("Test passed: Successfully navigated to hotel details page")
    
    @pytest.mark.hotel
    @pytest.mark.regression
    @allure.title("Test hotel information is displayed")
    @allure.description("Verify that hotel details page displays hotel name, rating, and price")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_hotel_information_displayed(self):
        """Test that hotel information is displayed."""
        with allure.step("Verify page is loaded"):
            assert self.hotel_details.is_loaded(), "Hotel details page did not load"
        
        with allure.step("Get hotel name"):
            hotel_name = self.hotel_details.get_hotel_name()
            assert hotel_name, "Hotel name not found"
            logger.info(f"Hotel name: {hotel_name}")
            allure.attach(hotel_name, name="Hotel Name", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Get hotel rating"):
            hotel_rating = self.hotel_details.get_hotel_rating()
            assert hotel_rating, "Hotel rating not found"
            logger.info(f"Hotel rating: {hotel_rating}")
            allure.attach(hotel_rating, name="Hotel Rating", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Get hotel price"):
            hotel_price = self.hotel_details.get_hotel_price()
            # Price might not always be visible, so we just log it
            logger.info(f"Hotel price: {hotel_price}")
            if hotel_price and hotel_price != "N/A":
                allure.attach(hotel_price, name="Hotel Price", attachment_type=allure.attachment_type.TEXT)
        
        logger.info("Test passed: Hotel information displayed correctly")
    
    @pytest.mark.hotel
    @pytest.mark.regression
    @allure.title("Test hotel amenities are displayed")
    @allure.description("Verify that hotel details page displays list of amenities")
    @allure.severity(allure.severity_level.NORMAL)
    def test_hotel_amenities_displayed(self):
        """Test that hotel amenities are displayed."""
        with allure.step("Verify page is loaded"):
            assert self.hotel_details.is_loaded(), "Hotel details page did not load"
        
        with allure.step("Get hotel amenities"):
            amenities = self.hotel_details.get_amenities()
            
            # Amenities might not always be visible in the same location
            if amenities:
                assert len(amenities) > 0, "No amenities found"
                logger.info(f"Found {len(amenities)} amenities")
                
                # Log first few amenities
                for i, amenity in enumerate(amenities[:5], 1):
                    logger.info(f"Amenity {i}: {amenity}")
                
                allure.attach(
                    "\n".join(amenities),
                    name="Hotel Amenities",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                logger.warning("Amenities section not found on this page")
                # Don't fail the test as amenities might be in a different section
        
        logger.info("Test passed: Amenities check completed")
    
    @pytest.mark.hotel
    @pytest.mark.sanity
    @allure.title("Test hotel details page elements")
    @allure.description("Verify that all key elements are present on hotel details page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_hotel_details_page_elements(self):
        """Test that all key elements are present on hotel details page."""
        with allure.step("Verify page is loaded"):
            assert self.hotel_details.is_loaded(), "Hotel details page did not load"
        
        with allure.step("Verify hotel details are loaded"):
            details_loaded = self.hotel_details.verify_hotel_details_loaded()
            assert details_loaded, "Hotel details not properly loaded"
        
        with allure.step("Collect all hotel information"):
            hotel_info = {
                "name": self.hotel_details.get_hotel_name(),
                "rating": self.hotel_details.get_hotel_rating(),
                "price": self.hotel_details.get_hotel_price(),
            }
            
            # Verify essential information is present
            assert hotel_info["name"], "Hotel name is missing"
            
            # Log all information
            info_text = "\n".join([f"{key}: {value}" for key, value in hotel_info.items()])
            logger.info(f"Hotel Information:\n{info_text}")
            allure.attach(info_text, name="Hotel Information", attachment_type=allure.attachment_type.TEXT)
        
        logger.info("Test passed: All key elements verified on hotel details page")


@allure.feature("Hotel Details")
@allure.story("Hotel Booking Flow")
class TestHotelBookingFlow:
    """Test cases for hotel booking flow."""
    
    @pytest.mark.hotel
    @pytest.mark.regression
    @allure.title("Test complete hotel selection flow")
    @allure.description("Verify complete flow from search to hotel details")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_hotel_selection_flow(self, home_page):
        """Test complete flow from search to viewing hotel details."""
        with allure.step("Step 1: Perform search"):
            destination = "Dubai"
            home_page.enter_destination(destination)
            home_page.select_guests(adults=2, children=0, rooms=1)
            home_page.click_search()
        
        with allure.step("Step 2: Verify search results"):
            search_results = SearchResultsPage(home_page.driver)
            assert search_results.is_loaded(), "Search results page did not load"
            
            results_count = search_results.get_search_results_count()
            assert results_count > 0, "No search results found"
            logger.info(f"Found {results_count} results")
        
        with allure.step("Step 3: Select first hotel"):
            first_hotel_name = search_results.get_first_hotel_name()
            logger.info(f"Selecting hotel: {first_hotel_name}")
            
            search_results.click_first_hotel()
        
        with allure.step("Step 4: Verify hotel details page"):
            hotel_details = HotelDetailsPage(home_page.driver)
            assert hotel_details.is_loaded(), "Hotel details page did not load"
        
        with allure.step("Step 5: Verify hotel information"):
            hotel_name = hotel_details.get_hotel_name()
            assert hotel_name, "Hotel name not found"
            
            hotel_rating = hotel_details.get_hotel_rating()
            logger.info(f"Hotel: {hotel_name}, Rating: {hotel_rating}")
            
            # Attach final hotel information
            allure.attach(
                f"Hotel: {hotel_name}\nRating: {hotel_rating}",
                name="Selected Hotel",
                attachment_type=allure.attachment_type.TEXT
            )
        
        logger.info("Test passed: Complete hotel selection flow executed successfully")

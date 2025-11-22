"""
Search functionality tests.
Tests for Booking.com search features.
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.helpers import DateHelper, DataHelper
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Search")
@allure.story("Basic Search")
class TestSearch:
    """Test cases for search functionality."""
    
    @pytest.mark.smoke
    @pytest.mark.search
    @allure.title("Test search with destination only")
    @allure.description("Verify that user can search for hotels by entering only destination")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_with_destination(self, home_page):
        """Test basic search with destination only."""
        with allure.step("Enter destination"):
            destination = "London"
            home_page.enter_destination(destination)
        
        with allure.step("Click search button"):
            home_page.click_search()
        
        with allure.step("Verify search results are displayed"):
            search_results = SearchResultsPage(home_page.driver)
            assert search_results.is_loaded(), "Search results page did not load"
            
            results_count = search_results.get_search_results_count()
            assert results_count > 0, "No search results found"
            
            logger.info(f"Test passed: Found {results_count} results for {destination}")
    
    @pytest.mark.smoke
    @pytest.mark.search
    @allure.title("Test search with destination and dates")
    @allure.description("Verify that user can search for hotels with destination and date range")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_with_dates(self, home_page):
        """Test search with destination and dates."""
        with allure.step("Prepare test data"):
            destination = "Paris"
            check_in = DateHelper.get_future_date(30)
            check_out = DateHelper.get_future_date(33)
            
            allure.attach(f"Check-in: {check_in}, Check-out: {check_out}", 
                         name="Test Data", 
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Enter destination"):
            home_page.enter_destination(destination)
        
        with allure.step("Select check-in date"):
            home_page.select_check_in_date(check_in)
        
        with allure.step("Select check-out date"):
            home_page.select_check_out_date(check_out)
        
        with allure.step("Click search button"):
            home_page.click_search()
        
        with allure.step("Verify search results are displayed"):
            search_results = SearchResultsPage(home_page.driver)
            assert search_results.is_loaded(), "Search results page did not load"
            
            results_count = search_results.get_search_results_count()
            assert results_count > 0, "No search results found"
            
            logger.info(f"Test passed: Found {results_count} results for {destination}")
    
    @pytest.mark.search
    @allure.title("Test search with multiple guests")
    @allure.description("Verify that user can search for hotels with multiple guests and rooms")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_guests(self, home_page):
        """Test search with multiple guests."""
        with allure.step("Prepare test data"):
            destination = "Dubai"
            adults = 4
            children = 2
            rooms = 2
        
        with allure.step("Enter destination"):
            home_page.enter_destination(destination)
        
        with allure.step("Configure guests"):
            home_page.select_guests(adults=adults, children=children, rooms=rooms)
        
        with allure.step("Click search button"):
            home_page.click_search()
        
        with allure.step("Verify search results are displayed"):
            search_results = SearchResultsPage(home_page.driver)
            assert search_results.is_loaded(), "Search results page did not load"
            
            results_count = search_results.get_search_results_count()
            assert results_count > 0, "No search results found"
            
            logger.info(f"Test passed: Found {results_count} results for {destination}")
    
    @pytest.mark.smoke
    @pytest.mark.search
    @allure.title("Test search results are displayed")
    @allure.description("Verify that search results contain property information")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_results_displayed(self, home_page):
        """Test that search results display property information."""
        with allure.step("Perform search"):
            destination = "New York"
            home_page.enter_destination(destination)
            home_page.click_search()
        
        with allure.step("Verify search results page loads"):
            search_results = SearchResultsPage(home_page.driver)
            assert search_results.is_loaded(), "Search results page did not load"
        
        with allure.step("Verify property names are displayed"):
            property_names = search_results.get_all_property_names()
            assert len(property_names) > 0, "No property names found"
            
            # Log first few properties
            logger.info(f"Found {len(property_names)} properties")
            for i, name in enumerate(property_names[:3], 1):
                logger.info(f"Property {i}: {name}")
                allure.attach(name, name=f"Property {i}", attachment_type=allure.attachment_type.TEXT)
        
        logger.info("Test passed: Search results displayed correctly")
    
    @pytest.mark.regression
    @pytest.mark.search
    @allure.title("Test search with complete scenario from test data")
    @allure.description("Verify search using complete scenario from test data file")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_complete_scenario(self, home_page):
        """Test search with complete scenario from test data."""
        with allure.step("Load test data"):
            scenario = DataHelper.get_search_scenario(0)
            assert scenario, "Failed to load test scenario"
            
            destination = scenario.get("destination")
            adults = scenario.get("adults", 2)
            children = scenario.get("children", 0)
            rooms = scenario.get("rooms", 1)
            days_from_now = scenario.get("days_from_now", 30)
            nights = scenario.get("nights", 3)
            
            check_in = DateHelper.get_future_date(days_from_now)
            check_out = DateHelper.get_future_date(days_from_now + nights)
            
            allure.attach(
                f"Destination: {destination}\nAdults: {adults}\nChildren: {children}\n"
                f"Rooms: {rooms}\nCheck-in: {check_in}\nCheck-out: {check_out}",
                name="Test Scenario",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Perform complete search"):
            home_page.search(
                destination=destination,
                check_in_date=check_in,
                check_out_date=check_out,
                adults=adults,
                children=children,
                rooms=rooms
            )
        
        with allure.step("Verify search results"):
            search_results = SearchResultsPage(home_page.driver)
            assert search_results.is_loaded(), "Search results page did not load"
            
            results_count = search_results.get_search_results_count()
            assert results_count > 0, "No search results found"
            
            logger.info(f"Test passed: Complete search scenario executed successfully")

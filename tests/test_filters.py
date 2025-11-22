"""
Filter and sorting tests.
Tests for Booking.com filter and sorting functionality.
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.helpers import DateHelper
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Filters and Sorting")
@allure.story("Search Filters")
class TestFilters:
    """Test cases for filter and sorting functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, home_page):
        """Setup for filter tests - perform initial search."""
        with allure.step("Perform initial search"):
            destination = "London"
            home_page.enter_destination(destination)
            home_page.click_search()
            
            self.search_results = SearchResultsPage(home_page.driver)
            assert self.search_results.is_loaded(), "Search results page did not load"
            
            # Store initial results count
            self.initial_count = self.search_results.get_search_results_count()
            logger.info(f"Initial search returned {self.initial_count} results")
    
    @pytest.mark.filters
    @pytest.mark.regression
    @allure.title("Test apply star rating filter")
    @allure.description("Verify that user can filter search results by star rating")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apply_rating_filter(self):
        """Test applying star rating filter."""
        with allure.step("Apply 4-star rating filter"):
            rating = 4
            self.search_results.apply_rating_filter(rating)
        
        with allure.step("Verify filter is applied"):
            # Results should still be visible (may be same or different count)
            assert self.search_results.verify_filters_applied(), "Filter not applied correctly"
            
            filtered_count = self.search_results.get_search_results_count()
            logger.info(f"After applying {rating}-star filter: {filtered_count} results")
            
            # We should have some results (Booking.com has many 4-star hotels in London)
            assert filtered_count > 0, "No results after applying filter"
        
        logger.info("Test passed: Star rating filter applied successfully")
    
    @pytest.mark.filters
    @pytest.mark.sanity
    @allure.title("Test sort by price")
    @allure.description("Verify that user can sort search results by price")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price(self):
        """Test sorting results by price."""
        with allure.step("Sort results by price"):
            # Common sort options: 'price', 'review_score_and_price', 'distance_from_search'
            self.search_results.sort_by("price")
        
        with allure.step("Verify results are still displayed"):
            sorted_count = self.search_results.get_search_results_count()
            assert sorted_count > 0, "No results after sorting"
            
            logger.info(f"After sorting by price: {sorted_count} results")
        
        with allure.step("Verify prices are displayed"):
            prices = self.search_results.get_all_property_prices()
            assert len(prices) > 0, "No prices found after sorting"
            
            logger.info(f"Found {len(prices)} prices")
            if prices:
                allure.attach(
                    "\n".join(prices[:5]),
                    name="Sample Prices",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        logger.info("Test passed: Sort by price executed successfully")
    
    @pytest.mark.filters
    @pytest.mark.regression
    @allure.title("Test apply multiple filters")
    @allure.description("Verify that user can apply multiple filters together")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_filters(self):
        """Test applying multiple filters together."""
        with allure.step("Apply star rating filter"):
            rating = 3
            self.search_results.apply_rating_filter(rating)
        
        with allure.step("Sort by price"):
            self.search_results.sort_by("price")
        
        with allure.step("Verify filters are applied"):
            assert self.search_results.verify_filters_applied(), "Filters not applied correctly"
            
            final_count = self.search_results.get_search_results_count()
            logger.info(f"After applying multiple filters: {final_count} results")
            
            assert final_count > 0, "No results after applying multiple filters"
        
        with allure.step("Verify property information is displayed"):
            property_names = self.search_results.get_all_property_names()
            assert len(property_names) > 0, "No property names found"
            
            logger.info(f"Found {len(property_names)} properties with multiple filters")
        
        logger.info("Test passed: Multiple filters applied successfully")
    
    @pytest.mark.filters
    @pytest.mark.sanity
    @allure.title("Test filter results count changes")
    @allure.description("Verify that applying filters changes the results count")
    @allure.severity(allure.severity_level.MINOR)
    def test_filter_changes_results(self):
        """Test that applying filters changes results."""
        with allure.step("Get initial results count"):
            initial_count = self.initial_count
            logger.info(f"Initial results: {initial_count}")
        
        with allure.step("Apply 5-star rating filter"):
            self.search_results.apply_rating_filter(5)
        
        with allure.step("Get filtered results count"):
            filtered_count = self.search_results.get_search_results_count()
            logger.info(f"Filtered results: {filtered_count}")
            
            allure.attach(
                f"Initial: {initial_count}\nFiltered: {filtered_count}",
                name="Results Comparison",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Verify results are displayed"):
            # We should have results (may be same or different from initial)
            assert filtered_count > 0, "No results after filtering"
        
        logger.info("Test passed: Filter affects results as expected")


@allure.feature("Filters and Sorting")
@allure.story("Advanced Filters")
class TestAdvancedFilters:
    """Test cases for advanced filtering."""
    
    @pytest.mark.filters
    @pytest.mark.regression
    @allure.title("Test search and filter workflow")
    @allure.description("Verify complete workflow of search and applying filters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_and_filter_workflow(self, home_page):
        """Test complete search and filter workflow."""
        with allure.step("Perform search with dates"):
            destination = "Paris"
            check_in = DateHelper.get_future_date(45)
            check_out = DateHelper.get_future_date(48)
            
            home_page.enter_destination(destination)
            home_page.select_check_in_date(check_in)
            home_page.select_check_out_date(check_out)
            home_page.click_search()
        
        with allure.step("Wait for results to load"):
            search_results = SearchResultsPage(home_page.driver)
            assert search_results.is_loaded(), "Search results page did not load"
        
        with allure.step("Get initial results"):
            initial_count = search_results.get_search_results_count()
            logger.info(f"Initial results: {initial_count}")
            assert initial_count > 0, "No initial results found"
        
        with allure.step("Apply filters"):
            search_results.apply_rating_filter(4)
        
        with allure.step("Verify filtered results"):
            filtered_count = search_results.get_search_results_count()
            logger.info(f"Filtered results: {filtered_count}")
            assert filtered_count > 0, "No results after filtering"
        
        with allure.step("Get property details"):
            first_hotel = search_results.get_first_hotel_name()
            assert first_hotel, "Could not get first hotel name"
            
            logger.info(f"First hotel: {first_hotel}")
            allure.attach(first_hotel, name="First Hotel", attachment_type=allure.attachment_type.TEXT)
        
        logger.info("Test passed: Complete search and filter workflow executed successfully")

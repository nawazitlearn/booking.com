"""
Pytest configuration and fixtures.
Contains setup, teardown, and common fixtures for all tests.
"""

import pytest
import allure
from datetime import datetime
from selenium.webdriver import Remote
from utils.driver_factory import DriverFactory
from utils.logger import Logger, get_logger
from utils.helpers import FileHelper
from config.config import Config
from pages.home_page import HomePage

logger = get_logger(__name__)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run browser in headless mode: true or false"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture with setup and teardown.
    
    Args:
        request: Pytest request object
        
    Yields:
        WebDriver instance
    """
    # Get command line options
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless").lower() == "true"
    
    # Create driver
    logger.info(f"Setting up driver: {browser} (headless: {headless})")
    driver_instance = DriverFactory.create_driver(browser=browser, headless=headless)
    
    # Log test start
    test_name = request.node.name
    Logger.log_test_start(test_name)
    
    yield driver_instance
    
    # Teardown
    logger.info("Tearing down driver")
    
    # Capture screenshot on failure
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        try:
            screenshot_path = FileHelper.save_screenshot(driver_instance, test_name)
            if screenshot_path:
                allure.attach.file(
                    str(screenshot_path),
                    name=f"failure_{test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
    
    # Log test end
    status = "PASSED" if not (hasattr(request.node, 'rep_call') and request.node.rep_call.failed) else "FAILED"
    Logger.log_test_end(test_name, status)
    
    # Quit driver
    DriverFactory.quit_driver(driver_instance)


@pytest.fixture(scope="function")
def home_page(driver):
    """
    HomePage fixture.
    
    Args:
        driver: WebDriver instance
        
    Returns:
        HomePage instance
    """
    page = HomePage(driver)
    page.open()
    return page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for screenshot on failure.
    
    Args:
        item: Test item
        call: Test call
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session", autouse=True)
def configure_allure_environment():
    """Configure Allure environment properties."""
    try:
        import platform
        from selenium import __version__ as selenium_version
        
        environment_properties = {
            "Browser": Config.BROWSER,
            "Platform": platform.system(),
            "Python Version": platform.python_version(),
            "Selenium Version": selenium_version,
            "Base URL": Config.BASE_URL,
            "Headless": str(Config.HEADLESS),
        }
        
        # Write environment properties for Allure
        allure_results_dir = Config.REPORTS_DIR / "allure-results"
        allure_results_dir.mkdir(exist_ok=True)
        
        env_file = allure_results_dir / "environment.properties"
        with open(env_file, 'w') as f:
            for key, value in environment_properties.items():
                f.write(f"{key}={value}\n")
        
        logger.info("Allure environment configured")
    except Exception as e:
        logger.warning(f"Failed to configure Allure environment: {e}")


def pytest_configure(config):
    """
    Pytest configuration hook.
    
    Args:
        config: Pytest config object
    """
    # Register custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression tests")
    config.addinivalue_line("markers", "sanity: Sanity tests")
    config.addinivalue_line("markers", "search: Search functionality tests")
    config.addinivalue_line("markers", "filters: Filter and sorting tests")
    config.addinivalue_line("markers", "hotel: Hotel details tests")


@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """Session-level setup."""
    logger.info("=" * 80)
    logger.info("TEST SESSION STARTED")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Browser: {Config.BROWSER}")
    logger.info(f"Base URL: {Config.BASE_URL}")
    logger.info("=" * 80)
    
    yield
    
    logger.info("=" * 80)
    logger.info("TEST SESSION COMPLETED")
    logger.info("=" * 80)

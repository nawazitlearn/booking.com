"""
Custom decorators module.
Provides decorators for logging, error handling, and retry logic.
"""

import functools
import time
import allure
from utils.logger import get_logger

logger = get_logger(__name__)


def log_action(func):
    """
    Decorator to log method entry and exit.
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.info(f"Executing: {func_name}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"Completed: {func_name}")
            return result
        except Exception as e:
            logger.error(f"Error in {func_name}: {str(e)}")
            raise
    
    return wrapper


def screenshot_on_failure(func):
    """
    Decorator to capture screenshot on failure.
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            # Assume self has driver attribute
            if hasattr(self, 'driver'):
                try:
                    from utils.helpers import FileHelper
                    screenshot_path = FileHelper.save_screenshot(
                        self.driver, 
                        func.__name__
                    )
                    if screenshot_path:
                        allure.attach.file(
                            str(screenshot_path),
                            name=f"failure_{func.__name__}",
                            attachment_type=allure.attachment_type.PNG
                        )
                except Exception as screenshot_error:
                    logger.error(f"Failed to capture screenshot: {screenshot_error}")
            raise
    
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Decorator to retry a function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
        exceptions: Tuple of exceptions to catch
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {str(e)}"
                        )
                        raise
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempts}/{max_attempts}), "
                        f"retrying in {delay}s: {str(e)}"
                    )
                    time.sleep(delay)
        
        return wrapper
    
    return decorator


def allure_step(step_title: str = None):
    """
    Decorator to add Allure step.
    
    Args:
        step_title: Custom step title (uses function name if not provided)
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            title = step_title or func.__name__.replace('_', ' ').title()
            with allure.step(title):
                return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def measure_time(func):
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result
    
    return wrapper

import vars
import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ( 
    TimeoutException, NoSuchElementException, WebDriverException, NoSuchWindowException
)

def navigate_to_login(browser):
    """Navigates to the LinkedIn login page."""
    try: 
        browser.get("https://www.linkedin.com/login")
        logging.info("Navigating to login")
        wait_for_page_load(browser)
    except TimeoutException as e:
        logging.error(f"Timeout while loading the page: {e}")
    except WebDriverException as e:
        logging.error(f"WebDriver exception occurred: {e}")
    except NoSuchWindowException as e:
        logging.error(f"No such window exception: {e}")

def wait_for_page_load(browser, timeout=10):
    """Waits for the page to fully load."""
    try:
        WebDriverWait(browser, timeout).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        logging.info("Load waiting")
    except TimeoutException:
        logging.error("Page load timed out")
        browser.quit()
        raise

def perform_login(browser):
    """Performs the login operation."""
    try:
        logging.info("Trying to login")
        username_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        username_field.send_keys(vars.username)
        password_field.send_keys(vars.password)
        sign_in_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        sign_in_button.click()
    except NoSuchElementException as e:
        logging.error(f"Login element not found: {e}")
        browser.quit()
        raise
    except TimeoutException as e:
        logging.error(f"Timeout while trying to find login elements: {e}")
        browser.quit()
        raise

def handle_checkpoint(browser):
    """Handles the checkpoint challenge (20sec for human interaction)."""
    while "checkpoint/challenge" in browser.current_url:
        logging.info("Challenge found. Waiting 20 secs")
        time.sleep(20)
        logging.info("Challenge waiting time exceeded")

def navigate_to_jobs(browser, url):
    """Navigates to the specific jobs page."""
    try:
        browser.get(str(url))
        logging.info("Navigating to jobs URL")
        wait_for_page_load(browser)
    except TimeoutException as e:
        logging.error(f"Timeout while loading the page: {e}")
    except WebDriverException as e:
        logging.error(f"WebDriver exception occurred: {e}")
    except NoSuchWindowException as e:
        logging.error(f"No such window exception: {e}")

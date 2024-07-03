import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ( 
    TimeoutException, NoSuchElementException, StaleElementReferenceException, 
    ElementClickInterceptedException, WebDriverException, NoSuchWindowException
)

from utils import set_filename, file_save
from navigation import navigate_to_jobs, wait_for_page_load

def extract_jobs(browser, job_url):
    """Extracts job IDs from the provided URL."""
    try:
        navigate_to_jobs(browser, job_url)
        job_ids = extract_job_ids(browser)
        return job_ids
    except TimeoutException:
        logging.error("Error during job extraction")
        return []

def extract_job_ids(browser):
    """Extracts data-job-id from job list items across all pages."""
    job_ids = []
    while True:
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.scaffold-layout__list-container"))
            )
            job_elements = browser.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container li")
            for job_element in job_elements:
                try:
                    job_id = job_element.get_attribute("data-occludable-job-id")
                    if job_id:
                        job_ids.append(job_id)
                        logging.debug("Processing job ID " + job_id)
                except StaleElementReferenceException:
                    logging.info("Stale element reference at " + job_id + ", trying to get the element again.")
                    job_elements = browser.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container li")
                    continue
            logging.info(f"Found {len(job_ids)} job(s)")
            if not go_to_next_page(browser):
                break
        except TimeoutException:
            logging.error("Timed out waiting for job list to load")
            break
    return job_ids

def go_to_next_page(browser):
    """Navigates to the next page of job listings, if available."""
    try:
        next_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-search-pagination__button--next"))
        )
        # Move to the next button to ensure it is visible
        ActionChains(browser).move_to_element(next_button).perform()
        try:
            next_button.click()
            logging.info("Browsing next page")
        except ElementClickInterceptedException:
            logging.info("Next button click intercepted, scrolling to button and trying again.")
            browser.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            next_button.click()
        wait_for_page_load(browser)
        return True
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
        logging.info("No more pages or next button not found.")
        return False

def check_job(browser, jobid):
    """Check for suitable jobs for relocation"""
    try:
        browser.get("https://www.linkedin.com/jobs/view/" + str(jobid))
        wait_for_page_load(browser)
        logging.info("Browsing https://www.linkedin.com/jobs/view/" + str(jobid))
    except TimeoutException as e:
        logging.error(f"Timeout while loading the page: {e}")
    except WebDriverException as e:
        logging.error(f"WebDriver exception occurred: {e}")
    except NoSuchWindowException as e:
        logging.error(f"No such window exception: {e}")

def click_show_qualification_details(browser):
    """Clicks the 'Show qualification details' button to open the modal."""
    try:
        show_details_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='artdeco-button__text' and text()='Show qualification details']"))
        )
        show_details_button.click()
        time.sleep(5)
    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
        logging.error(f"Error clicking 'Show qualification details' button: {e}. Ignoring entry")
        return False
    return True

def extract_skills_from_modal(browser):
    """Extracts the text from all divs inside li elements within the modal."""
    skill_texts = []
    try:
        # Wait for the modal to be visible
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'job-details-skill-match-modal__content')]"))
        )
        # Find all li elements within the specified structure
        li_elements = browser.find_elements(By.XPATH, "//div[contains(@class, 'job-details-skill-match-modal__content')]//li")
        logging.info(f"Found {len(li_elements)} skill(s)")
        for li in li_elements:
            try:
                # Extract the text from the div inside each li
                div_element = li.find_element(By.XPATH, ".//div[2]")
                logging.debug(f"Scraped skill: {div_element.text}")
                skill_texts.append(str(div_element.text))
            except NoSuchElementException:
                logging.error("No skills found!")
                continue
    except TimeoutException:
        logging.error("Timed out waiting for skill details to load")
    return skill_texts

def extract_skills_from_jobs(browser, job_ids, job_url):
    """Extracts skills from job postings."""
    if not job_ids:
        logging.warning("Job buffer empty")
        return []

    curfile = set_filename(job_url)
    total = len(job_ids)
    skills = []

    for i, job in enumerate(job_ids):
        percent = i / total * 100
        logging.info(f'Processing status: {percent:.2f}% ({i + 1}/{total})')
        check_job(browser, job)
        click_show_qualification_details(browser)
        skills.append(extract_skills_from_modal(browser))
        file_save(curfile, skills)
    return skills
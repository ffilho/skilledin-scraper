import logging

from selenium.common.exceptions import TimeoutException

from utils import initiate_browser, quit_browser, set_job_url, handle_login, save_to_excel
from process import process_all_skills
from extraction import extract_jobs, extract_skills_from_jobs
from process import process_skills_from_file, process_all_files
from vars import default_job_url, cookies_file

def display_menu():
    """Displays the menu options."""
    print("\nMenu:")
    print("1. Set job URL query")
    print("2. Extract jobs & skills")
    print("3. Process extracted skills")
    print("4. Process skills from single file")
    print("5. Process skills from all files")
    print("6. Exit")

def menu():
    """Displays a menu and executes the chosen option."""
    job_url = default_job_url
    browser = None
    job_ids = []
    skills = []

    while True:
        display_menu()

        print("\nCurrent job search: " + job_url)

        choice = input("\nYour option: (1-6): ")

        if choice == '1':
            job_url = set_job_url(default_job_url)
        elif choice == '2':
            browser = initiate_browser()
            try:
                handle_login(browser, cookies_file)
                job_ids = extract_jobs(browser, job_url)
                if browser:
                    skills = extract_skills_from_jobs(browser, job_ids, job_url)
                else:
                    logging.warning("Browser is not initiated.")
            except:
                if browser:
                    quit_browser(browser)
                    logging.error("Unable to process.")
        elif choice == '3':
            if skills:
                skillsbuffer = process_all_skills(skills)
                print("\nTotal processed jobs: " + str(skillsbuffer[1]) + "\n")
                print(skillsbuffer[0])
                xlsexport = input("\nExport to XLS (y/n): ")
                if xlsexport == 'y':
                    try:
                        save_to_excel(skillsbuffer[0], job_url, skillsbuffer[1])
                    except:
                        logging.error("Cannot export to XLS.")
                else:
                    logging.info("Skipping export.")
            else:
                logging.warning("Skill buffer is empty.")
        elif choice == '4':
            skillsbuffer = process_skills_from_file()
            if skillsbuffer is not None:
                print("\nTotal processed jobs: " + str(skillsbuffer[0][1]) + "\n")
                print(skillsbuffer[0][0])
                xlsexport = input("\nExport to XLS (y/n): ")
                if xlsexport == 'y':
                    try:
                        save_to_excel(skillsbuffer[0][0], skillsbuffer[1], skillsbuffer[0][1])
                    except:
                        logging.error("Cannot export to XLS.")
                else:
                    logging.info("Skipping export.")
            else:
                logging.warning("No valid file processed.")
        elif choice == '5':
            skillsbuffer = process_all_files()
            if skillsbuffer is not None:
                print("\nTotal processed jobs: " + str(skillsbuffer[1]) + "\n")
                print(skillsbuffer[0])
                xlsexport = input("\nExport to XLS (y/n): ")
                if xlsexport == 'y':
                    try:
                        save_to_excel(skillsbuffer[0], 'all-files', skillsbuffer[1])
                    except:
                        logging.error("Cannot export to XLS.")
                else:
                    logging.info("Skipping export.")
            else:
                logging.warning("No valid file processed.")                
        elif choice == '6':
            if browser:
                quit_browser(browser)
                logging.debug("Browser closed successfully...")
            break
        else:
            logging.warning("Invalid entry")

def main():
    """Main function to control the flow of the script."""
    try:
        menu()
    except TimeoutException:
        logging.error("Error during processing")

if __name__ == "__main__":
    main()
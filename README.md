# SkilledIn - LinkedIn Skills scraper

(very) Simple scraper to obtain relevant skills for your future job.

## Summary

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About

Skills are important for those seeking better positioning when looking for a job. Additionally, a well-filled profile with relevant skills has a better qualification on LinkedIn's SSI.

Everyone knows that identifying skills for all your jobs is a pain in the neck. It is a time-consuming activity, and often the jobs you are seeking do not even use the skills you have defined.

To avoid this exhausting work, it is easier to search for job opportunities that make sense for you and use the skills listed there to enrich your profile. However, this is also a time-consuming activity.

To solve this problem, I created this simple scraper. Based on a search URL, it accesses all the listed jobs and extracts the skills, sorting them by recurrence within all jobs, helping you identify which skills are crucial for your desired position.

**By the end of the day, I'll have something like:** skill, how many times it appears in all the jobs for the given search, and the percentage of relevance for these skills.

The goal is to use the date to create a concise list of skills that make sense for the positions you are seeking.

Attention: LinkedIn has a limit of 100 skills per profile. Keep this in mind when defining the size of your final list.

## Installation

Step-by-step instructions for installing skilledin:

1. Clone the repository:
   ```sh
   git clone https://github.com/ffilho/skilledin-scraper.git
   cd skilledin-scraper
2. Ensure you have pip installed:
    ```sh
    python -m ensurepip --upgrade
3. Create your virtual environment:
    ```sh
    python -m venv venv
4. Activate your virtual environment:
    ```sh
    source venv/bin/activate
5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
6. Create a file named `vars.py` inside `src`. This file should have the following format:
    ```python
    # vars.py
    import logging

    # LinkedIn Credentials
    username = "your-linkedin-email"
    password = "your-linkedin-password"
    #You can inspect the code/traffic. I'm not stealing your credentials. I'm a gentleman.

    # Specific stopwords for skills
    # Example: 
    # stopwords = {'and', 'the', 'with', 'a', 'an', 'of', 'to', 'in', 'for'}
    stopwords = {}

    # Default search string
    default_job_url = "https://www.linkedin.com/jobs/collections/recommended/"

    # Cookies filename
    cookies_file = "cookies.json"

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Folder configuration
    ext_folder = "./extract/"
    exp_folder = "./export/"
    
## Usage
1. Run `main.py` inside `src`. Selenium will start Chrome and chromedriver, and you can interact with the browser if necessary.

2. The login is performed automatically with the credentials provided in `vars.py`. To avoid the login process each time you run the script, session cookies will be saved in the `src` directory.

   **Important:** Your cookies are as important as your credentials. Protect these files!

3. The script is programmed to wait for human input in the browser if any LinkedIn challenges appear on the screen. You may be asked to solve a captcha or authorize the session on your mobile device. The script will wait for you.

4. The default job search URL is the LinkedIn recommended jobs context. You can perform a more refined search on the site and copy the URL. To change it, use option **1** in the menu. If you want to proceed with the recommended jobs, skip this step.

5. To extract jobs & skills from the provided search, choose option **2** in the menu. The processing is displayed in the console and the browser. You can check if the script is behaving as expected and if your search provides relevant jobs. If necessary, stop the script with Ctrl+C. At the end of the processing, the results will be available in a text file within `src/extract`. 

6. By the end of extraction you can process the extracted data via option **3**. After processing it, you also can also export the data to an XLSX file.

6. Options **4** and **5** in the menu operate with previously saved files. You can perform several extractions and process them later, all-at-once or individually.

## Contributing
Feel free to fork this thing. If you can help me learn something from your contributions, I swear I'll become your friend.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE) - see the LICENSE file for details.

This means you are free to use, modify, and distribute this software, as long as any distributed versions or derivative works are also licensed under the GNU GPL v3.0. This ensures that all versions of this software remain free and open source.

Copyleft ensures that the same freedoms are preserved in all copies and derivatives of the software, fostering an environment of collaboration and shared improvement.

For more details, see the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Contact

Did you like this thing? Give me a shout on LinkedIn [https://www.linkedin.com/in/faustoafilho/](https://www.linkedin.com/in/faustoafilho/)!

If I helped you in any way, an endorsement in some skill over there would be greatly appreciated. :)

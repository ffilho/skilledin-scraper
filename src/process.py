import logging
import ast
import re
import pandas as pd

from collections import Counter

from vars import stopwords, ext_folder
from utils import list_files_in_directory

def preprocess_skill(skill):
    """Normalizes and cleans a skill string."""
    skill = re.sub(r'\s+', ' ', skill)  # Removes extra spaces
    return skill.strip()  # Removes leading and trailing spaces

def process_all_skills(file_path_or_list, stopwords=stopwords):
    """
    Processes all skills from a file or a list and returns the most common skills.
    
    Args:
        file_path_or_list (str or list): Path to the input file or a list of strings.
        stopwords (set): Set of irrelevant words to be filtered out.
    
    Returns:
        pd.DataFrame: DataFrame with all skills, counts, and percentages.
    """
    if isinstance(file_path_or_list, str):
        # 1. Load Data from file
        with open(file_path_or_list, 'r') as file:
            content = file.read()
        lines = content.split('\n')
        jobtotal = len(lines)
        lists_of_strings = [ast.literal_eval(line) for line in lines if line]
    elif isinstance(file_path_or_list, list):
        # Load Data from list
        lists_of_strings = [item for item in file_path_or_list if item != []]
        jobtotal = len(lists_of_strings)
    else:
        raise ValueError("file_path_or_list must be either a file path (str) or a list of strings")

    all_strings = []
    for sublist in lists_of_strings:
        all_strings.extend(sublist)
    
    # Preprocess and filter skills
    all_strings = [preprocess_skill(skill) for skill in all_strings if preprocess_skill(skill) not in stopwords]
    
    # 2. Count Frequencies
    string_counts = Counter(all_strings)
    all_skills_df = pd.DataFrame(string_counts.items(), columns=['Skill', 'Count'])
    all_skills_df['Percentage'] = (all_skills_df['Count'] / jobtotal * 100).round(0).astype(int)

    # Sort DataFrame by Count column in descending order
    all_skills_df = all_skills_df.sort_values(by='Count', ascending=False)

    # Set pandas option to display all rows
    pd.set_option('display.max_rows', None)
    return all_skills_df.reset_index(drop=True), jobtotal

def process_skills_from_file():
    """Processes skills from a selected file."""
    files = list_files_in_directory(ext_folder)

    if not files:
        logging.info("No files found in the directory.")
        return None

    print("\nFiles found:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")

    file_choice = input("\nEnter the number of the file you want to process: ")
    try:
        file_index = int(file_choice) - 1
        if 0 <= file_index < len(files):
            file_path = files[file_index]
            filebuffer = process_all_skills(file_path)
            return filebuffer, file_path 
        else:
            logging.warning("Invalid file number.")
    except ValueError:
        logging.warning("Invalid input. Please enter a number.")
        return None
    

def process_all_files():
    files = list_files_in_directory(ext_folder)

    if not files:
        logging.info("No files found in the directory.")
        return None

    all_files_content = []

    for file in files:
        with open(file, 'r') as f:
            content = f.read().replace('\n', '')
            all_files_content.append(content)

    combined_content = ''.join(all_files_content).replace('][', '],[')
    list_strings = combined_content.split('],[')

    list_strings = ['[' + s if not s.startswith('[') else s for s in list_strings]
    list_strings = [s + ']' if not s.endswith(']') else s for s in list_strings]

    valid_lists = []
    for s in list_strings:
        stack = []
        balanced = True
        for char in s:
            if char == '[':
                stack.append(char)
            elif char == ']':
                if not stack:
                    balanced = False
                    break
                stack.pop()
        if balanced and not stack:
            try:
                valid_lists.append(ast.literal_eval(s))
            except SyntaxError:
                logging.warning(f"Syntax error when parsing: {s}")
        else:
            logging.warning(f"Unbalanced brackets in: {s}")
    
    processed_skills = process_all_skills(valid_lists)
    
    return processed_skills
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
from scores import calculate_score, stop_words, positive_words, negative_words, count_stop_words, count_sentences
from scores import complexWords, sum_total_characters, count_personal_pronouns, total_syllables_in_text
import openpyxl
from selenium.common.exceptions import NoSuchElementException


def extract_title_and_text(url):
    # Set up options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Open the URL
        driver.get(url)

         # Check if page is not found
        if "404" in driver.title or "Page Not Found" in driver.title:
            return "NONE", "NONE"
        
        # Extract the title
        title = driver.title
        try:   
            # Extract the body text
            body_text = driver.find_element(By.CLASS_NAME, 'td-post-content').text
        except NoSuchElementException:
            body_text = "NONE"
        return title, body_text
    finally:
        # Quit the WebDriver
        driver.quit()

# Example usage

# Load the Excel file
file_path = 'Input.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Ensure the columns are correctly named
df.columns = ['URL_ID', 'URL']

wb = openpyxl.Workbook()

# Create a new sheet
sheet = wb.active

# Header row
header = ["URL_ID", "URL", "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score", "Average Sentence Length", "Percentage of complex word", "Fog Index", "Average number of words per sentence", "Complex word count", "word count", "Syllable per word", "Personal Pronouns", "Average Word Length"]

from openpyxl.styles import Font

sheet.append(header)
for cell in sheet[1]:
    cell.font = Font(bold=True)

# Iterate through the URLs
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    title, text = extract_title_and_text(url)
    
    total_words = len(text.split())
    complex_words = complexWords(text)
    positive_score = calculate_score(text, stop_words, positive_words)
    negative_score = calculate_score(text, stop_words, negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / ((total_words - count_stop_words(text, stop_words)) + 0.000001)
    averageSentenceLength = total_words / count_sentences(text)
    percentageOfComplexWords = complex_words / total_words
    fogIndex = 0.4 * (percentageOfComplexWords + averageSentenceLength)
    averageNumWordsSentences = averageSentenceLength
    complexWordCount = complex_words
    avgWordLength = sum_total_characters(text) / total_words
    personalPronouns = count_personal_pronouns(text)
    syllPerWord = total_syllables_in_text(text) / total_words


    uploder = {'URL_ID' : url_id, 
               'URL' : url,
               'Positive Score' : positive_score,
               'Negative Score' : negative_score,
               'Polarity Score' : polarity_score,
               'Subjectivity Score' : subjectivity_score,
               'Average Sentence Length' : averageSentenceLength,
               'Percentage of complex word' : percentageOfComplexWords,
               'Fog Index' : fogIndex,
               'Average number of words per sentence' : averageNumWordsSentences,
               'Complex word count' : complexWordCount,
               'word count' : total_words,
               'Syllable per word' : syllPerWord,
               'Personal Pronouns' : personalPronouns,
               'Average Word Length' : avgWordLength,
               }

    
    sheet.append(list(uploder.values()))
    print(url_id)

wb.save("output.xlsx")
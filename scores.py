import os, re

def load_words_from_file(file_path):
    """Load words from a given file and return a set of words."""
    with open(file_path, 'r') as file:
        words = {line.strip() for line in file}
    return words

def load_stop_words(directory):
    """Load stop words from multiple text files in a given directory."""
    stop_words = set()
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        stop_words.update(load_words_from_file(file_path))
    return stop_words

def loading_words(file_path):
    """Load positive words from a given file."""
    return load_words_from_file(file_path)

def calculate_score(text, stop_words, positive_words):
    """Calculate the positive word score for the given text."""
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    positive_word_count = sum(1 for word in filtered_words if word.lower() in positive_words)
    return positive_word_count

def count_stop_words(text, stop_words):
    """Count the number of stop words in the given text."""
    words = text.split()
    stop_word_count = sum(1 for word in words if word.lower() in stop_words)
    return stop_word_count

def count_sentences(text):
    """Count the number of sentences in the given text."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [sentence for sentence in sentences if sentence.strip()]  # Remove empty sentences
    return len(sentences)

def count_syllables(word):
    """Count the number of syllables in a given word, considering exceptions."""
    word = word.lower()
    syllable_count = 0
    vowels = "aeiouy"
    
    if word.endswith(('es', 'ed')) and len(word) > 2 and word[-3] not in vowels:
        word = word[:-2]
        
    if word[0] in vowels:
        syllable_count += 1
    
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
            
    if word.endswith('e'):
        syllable_count = max(1, syllable_count - 1)
        
    return syllable_count

def count_syllables_in_text(text):
    """Count the number of syllables for each word in the given text."""
    words = text.split()
    syllable_counts = {word: count_syllables(word) for word in words}
    return syllable_counts

def complexWords(text):
    """Count the number off words with more than two syllables in the given text."""
    words = text.split()
    count = sum(1 for word in words if count_syllables(word) > 2)
    return count

def sum_total_characters(text):
    """Sum the total number of characters of each word in the text."""
    words = text.split()
    total_characters = sum(len(word) for word in words)
    return total_characters

def count_personal_pronouns(text):
    """Count the number of personal pronouns in the given text, excluding the country name 'US'."""
    personal_pronouns = re.findall(r'\b(I|me|my|us|our)\b', text, re.IGNORECASE)
    pronoun_count = len(personal_pronouns)
    return pronoun_count

def total_syllables_in_text(text):
    """Count the total number of syllables in the given text, considering exceptions."""
    words = text.split()
    total_syllables = sum(count_syllables(word) for word in words)
    return total_syllables

# Directory containing the stop word files
stop_words_directory = 'E:\Blackcoffer\stop words'
# File containing the positive words
positive_words_file = 'positive-words.txt'
negative_words_file = 'negative-words.txt'
# Example text to analyze
text_to_analyze = "This is an example text that will be used to calculate abundant the positive word score."

# Load stop words and positive words
stop_words = load_stop_words(stop_words_directory)
positive_words = loading_words(positive_words_file)
negative_words = loading_words(negative_words_file)

# # Calculate positive word score
# positive_score = calculate_score(text_to_analyze, stop_words, positive_words)
# negative_score = calculate_score(text_to_analyze, stop_words, negative_words)
# negative_score = count_stop_words(text_to_analyze, stop_words)

# polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

# print("Positive word score:", positive_score)
# print("Negative word score:", type(negative_score))
# print("Polarity score:", polarity_score)


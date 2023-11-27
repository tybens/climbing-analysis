import pickle 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string

def pickle_dump(obj, filename):
    with open('data/' + filename + '.pickle', 'wb') as f:
        pickle.dump(obj, f)


def pickle_load(filename):
    with open('data/' + filename + '.pickle', 'rb') as f:
        return pickle.load(f)

# --- HELPFUL FUNCTIONS FOR FORUM POSTS --- #


# --- VISUALIZATION FUNCTIONS FOR FORUM POSTS --- #


def descriptive_stats(df):
    '''
    Plots descriptive statistics for the dataframe
    '''

    # Create a figure with 3 subplots
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
    ax = ax.flatten()

    # Distribution of likes
    sns.histplot(df['num_likes'].astype(int), ax=ax[0])
    ax[0].set_title('Distribution of Likes')


    # Distribution of mean_word_length
    sns.histplot(df['mean_sent_length'], ax=ax[1])
    ax[1].set_title('Distribution of Mean Sentence Length')

    # Distribution of mean_word_length
    sns.histplot(df['mean_word_length'], ax=ax[2])
    ax[2].set_title('Distribution of Mean Word Length')

    # Distribution of word_count
    sns.histplot(df['word_count'], ax=ax[3])
    ax[3].set_title('Distribution of Word Count')

    # Adjust layout
    plt.tight_layout()
    plt.show()



# Function to remove punctuation from each word
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def word_freq_graph(all_text, top_n, title):
    # Removing punctuation and then splitting the text into words
    cleaned_words = [remove_punctuation(word).lower() for word in all_text.split() if remove_punctuation(word).lower() not in ENGLISH_STOP_WORDS]

    cleaned_words = [word for word in cleaned_words if word.strip()]
    # Recounting word frequencies with cleaned words
    cleaned_word_freq = Counter(cleaned_words)

    # Sorting words by frequency in descending order
    sorted_cleaned_word_freq = dict(sorted(cleaned_word_freq.items(), key=lambda item: item[1], reverse=True))

    # Selecting the top N words for the graph to avoid clutter
    top_cleaned_words = list(sorted_cleaned_word_freq.keys())[:top_n]
    top_cleaned_freqs = list(sorted_cleaned_word_freq.values())[:top_n]

    # Plotting the cleaned graph
    plt.figure(figsize=(10, 6))
    plt.bar(top_cleaned_words, top_cleaned_freqs)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    plt.title(title)
    plt.show()

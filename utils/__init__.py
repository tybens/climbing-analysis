import pickle 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


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
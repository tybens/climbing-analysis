from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import pandas as pd
import numpy as np
import csv
from nltk import tokenize

from bs4 import BeautifulSoup

import argparse
from utils import pickle_load, pickle_dump 

    
def get_post_urls(base, num_pages):
    forum_post_urls = []
    ext = "?page="

    for i in range(1, num_pages + 1):
        try:
            page = urlopen(base+ext+str(i)).read()
            soup = BeautifulSoup(page, 'html.parser')
            forum_post_urls.extend([i.td.a.get('href') for i in soup.find_all('tr')[1:]])
        except Exception as e:
            print(e)
            pass
        
    return forum_post_urls

def get_messages_from_thread(thread_url):
    # get all posts from thread  
    try:
        page = urlopen(thread_url).read()
        soup = BeautifulSoup(page, 'html.parser')
        title = soup.find('h1').get_text()

        messages = soup.find_all('tr')
        pagination = soup.find('div', class_='pagination').find_all('a')
    except Exception as e:
        pagination = []
        messages = []
        title = ''
        print(e)
        pass
    # if there is more than one page, get the rest of the messages on each page
    if len(pagination) > 1:
        num_pages = int(pagination[2].get_text().strip().split(' ')[-1])
        for i in range(2, num_pages + 1):
            try: 
                page = urlopen(thread_url + '?page=' + str(i)).read()
                soup = BeautifulSoup(page, 'html.parser')
                messages.extend(soup.find_all('tr'))
            except Exception as e:
                print(e)
                pass

    return messages, title

def get_data_from_message(message):
    """Extracts data from a message in a thread"""

    bio = message.find('div', class_='bio text-truncate')
    info = [i.strip() for i in bio.find('span', class_='text-warm small').text.replace('\t', '').replace('\n', '').split('·')[1:]]

    post_id = thread_url.split('/')[-2]
    date = info[0] 
    username = bio.find('strong').text
    body = message.find('div', class_='fr-view').text
    try:
        num_likes = message.find('span', class_='num-likes').text.replace('\n', '').strip()
    except:
        num_likes = 'post removed'
    location = info[1]
    joined = info[2][7:]
    points = info[3]
    

    clubs_imgs = message.find('div', class_='club').find_all('a')
    clubs = []
    for club in clubs_imgs:
        clubs.append(club.img.get('title'))
    clubs_str = ', '.join(clubs)

    column = [post_id, date, username, body, num_likes, location, joined, points, clubs_str]
    return column


import datetime
def subtract_days_from_current(x):
    # Get current date
    current_date = datetime.date.today()
    
    # Subtract x days
    new_date = current_date - datetime.timedelta(days=x)
    
    # Format the date
    formatted_date = new_date.strftime("%b %d, %Y")
    
    return formatted_date

def clean_and_generate_df(data, COLUMNS):
    df = pd.DataFrame(data, columns=COLUMNS)
    # --- cleaning body ---
    df.loc[:, 'body'] = df.body.str.replace('\n', '').str.replace('\xa0', '').str.strip()
    df = df[df.body.str.len() > 0]
    # --- cleaning date ---
    days_ago = df.date[['day' in i for i in df.date.values]]
    if len(days_ago):
        df.date[['day' in i for i in df.date.values]] = pd.to_numeric(days_ago.str[0]).apply(subtract_days_from_current)
    df.date[df.date.str.contains('ago')] = [datetime.date.today().strftime("%b %d, %Y") for _ in df.date[df.date.str.contains('ago')]]
    df.date = pd.to_datetime(df.date)
    # --- typeing --- 
    df['points'] = df['points'].str[-1].astype(int)
    df.num_likes.replace('post removed', 0, inplace=True)
    df.num_likes = df.num_likes.astype(int) 
    df.body = df.body.astype(str)
    # --- adding columns --- 
    df['mean_word_length'] = df.body.map(lambda rev: np.mean([len(word) for word in rev.split()]))
    df['mean_sent_length'] = df.body.map(lambda text: np.mean([len(tokenize.word_tokenize(sent)) for sent in tokenize.sent_tokenize(text)]))
    df['word_count'] = df.body.map(lambda text: len(tokenize.word_tokenize(text)))
    # --- dealing with NaNs ---
    df.clubs.fillna('', inplace=True)   
    df.title.fillna('', inplace=True)
    


    return df

# --- HELPER FUNCTIONS --- #

def load_and_concatenate_temp_data(base, files):
    """
    Loads all temporary csv files and concatenates them into a dataframe.
    """
    data = pd.DataFrame()
    for file in files:
        new_data = pd.read_csv(base + '_temp_' + file + '.csv')
        data = pd.concat([data, new_data], axis=0)

    # clean the raw, concatenated data and generate a dataframe
    COLUMNS = ['post_id', 'date', 'username', 'body', 'num_likes', 'location', 'joined', 'points', 'clubs','title']
    df = clean_and_generate_df(data, COLUMNS)
    return df


if __name__ == '__main__':
    # extract argument from command line for forum_name using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--forum_name', help='name of forum to scrape')
    # argument for num_pages, int
    parser.add_argument('-n', '--num_pages', type=int, help='number of pages to scrape')
    # warm start argument
    parser.add_argument('-w', '--warm_start', type=bool, default=False, help='whether to start from forum thread urls already scraped')
    parser.add_argument('-t', '--thread_start', type=int, default=0, help='Which forum thread url to start from.')

    args = parser.parse_args()
    # form base url
    BASE = "https://www.mountainproject.com/forum/" + str(args.forum_name)
    NUM_PAGES = args.num_pages
    FORUM_NAME_STR = args.forum_name.split("/")[-1]
    COLUMNS = ['post_id', 'date', 'username', 'body', 'num_likes', 'location', 'joined', 'points', 'clubs','title']

    # get all post urls
    if not args.warm_start:
        forum_post_urls = get_post_urls(BASE, NUM_PAGES)
        pickle_dump(forum_post_urls, f'{FORUM_NAME_STR}_urls')
        print("Dumped Thread urls to pickle file")
    else:
        forum_post_urls = pickle_load(f'{FORUM_NAME_STR}_urls')
        print("Loaded Thread urls from pickle file")

    # initialize temporary csv file and write the columns to, name it using a randint
    TEMP_FILE_NAME = f'data/temp/{FORUM_NAME_STR}_temp_{np.random.randint(100000)}.csv'
    with open(TEMP_FILE_NAME, 'w') as f:
        f.write(','.join(COLUMNS) + '\n')
    

    df = []
    for i, thread_url in enumerate(forum_post_urls[args.thread_start:]):      
        # get all messages from thread  
        print(f"Scraping thread {i+1 + args.thread_start} of {len(forum_post_urls)}")
        messages, title = get_messages_from_thread(thread_url)
        print(f"Found {len(messages)} messages in thread")
        new_data = []
        for message in messages:
            try:
                column = get_data_from_message(message)
                column.append(title)
                new_data.append(column)
            except Exception as e:
                print(e)
                pass

        df.extend(new_data)
        # write raw df to temporary csv file using open
        with open(TEMP_FILE_NAME, 'a', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in new_data:
                csv_writer.writerow(row)
        print(f"Dumped {len(new_data)} rows to temporary csv file")




    
    df = clean_and_generate_df(df, COLUMNS)
    df.to_csv(f'data/{FORUM_NAME_STR}.csv', index=False)

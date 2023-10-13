from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import pandas as pd
import numpy as np

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
    page = urlopen(thread_url).read()
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('h1').get_text()

    messages = soup.find_all('tr')
    pagination = soup.find('div', class_='pagination').find_all('a')
    # if there is more than one page, get the rest of the messages on each page
    if len(pagination) > 1:
        num_pages = int(pagination[2].get_text().strip().split(' ')[-1])
        for i in range(2, num_pages + 1):
            page = urlopen(thread_url + '?page=' + str(i)).read()
            soup = BeautifulSoup(page, 'html.parser')
            messages.extend(soup.find_all('tr'))

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

if __name__ == '__main__':
    # extract argument from command line for forum_name using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--forum_name', help='name of forum to scrape')
    # argument for num_pages, int
    parser.add_argument('-n', '--num_pages', type=int, help='number of pages to scrape')
    args = parser.parse_args()
    # form base url
    base = "https://www.mountainproject.com/forum/" + str(args.forum_name)
    num_pages = args.num_pages
    # get all post urls
    forum_post_urls = get_post_urls(base, num_pages)

    pickle_dump(forum_post_urls, f'{args.forum_name.split("/")[-1]}_urls.pkl')
    print("Dumped Thread urls to pickle file")

    df = []
    for i, thread_url in enumerate(forum_post_urls):      
        # get all messages from thread  
        print(f"Scraping thread {i+1} of {len(forum_post_urls)}")
        messages, title = get_messages_from_thread(thread_url)
        print(f"Found {len(messages)} messages in thread")
        for message in messages:
            try:
                column = get_data_from_message(message)
                column.append(title)
                df.append(column)
            except Exception as e:
                print(e)
                pass




    columns = ['post_id', 'date', 'username', 'body', 'num_likes', 'location', 'joined', 'points', 'clubs','title']
    df = pd.DataFrame(df, columns=columns)
    df.loc[:, 'body'] = df.body.apply(lambda x: x.replace('\n', ''))
    days_ago = df.date[['days' in i for i in df.date.values]]
    if len(days_ago):
        df.date[['days' in i for i in df.date.values]] = pd.to_numeric(days_ago.str[0]).apply(subtract_days_from_current)
    df['mean_word_length'] = df.body.map(lambda rev: np.mean([len(word) for word in rev.split()]))

    df.to_csv(f'data/{args.forum_name.split("/")[-1]}.csv', index=False)


import requests
from urllib.request import urlopen
import pandas as pd
import argparse

from bs4 import BeautifulSoup

def get_classics_from_area(classics_url):
    page = urlopen(classics_url).read()
    soup = BeautifulSoup(page, features='lxml')
    climb_urls = [i.find('a').get('href') for i in soup.find_all('tr', class_='route-row')]
    return climb_urls


def get_comments_on_route(route_id):
    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Alt-Used': 'www.mountainproject.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.mountainproject.com/route/105871977/bedtime-for-bonzo',
    'Cookie': 'photoIds=eyJpdiI6Ijd5SE9yeE5DbVcySk9iUitkMjQ5RWc9PSIsInZhbHVlIjoiQ29EU05xNk9tTmNXWlVEeHM5bGlobEkwYnBHU2lhdzVGU3o5YWRmZ2pmSnAvUWhmbkdjMWlSY0E2eWlEaDdjcSIsIm1hYyI6IjRmYTY3YjYzMGJhMGNmYmQ2ZDI2NjI3YzQ2ZDk1YmI4OWZkZjE1ZmRmY2JkZGQ1MTBkYzEyN2U5MjFkZjMwMjYiLCJ0YWciOiIifQ%3D%3D; photosTitle=Nearby%20Photos; prefs=%5BrouteSort%7Clr%5D%5BnavFilter%7CSport%5D%5BRFdiffMinrock%7C1000%5D%5BRFdiffMaxrock%7C4800%5D%5BRFstars%7C0%5D%5BRFtype%7Crock%5D%5BRFsort1%7Cpopularity%20desc%5D%5BRFsort2%7Crating%5D%5BmapX%7C-5348886%5D%5BmapY%7C4213856%5D%5BmapZoom%7C1.7%5D%5BcommentSort%7Coldest%5D; user=eyJpdiI6IjRWOGdEVk9aZWpiNEZjR2h5eHhyZ1E9PSIsInZhbHVlIjoiOTBPUVdkU3EvNlZsNkNieVJEUGF6UURqTWU0SVR4Q2JiMVRCbjIrdzdxOFY2dEFzNlAzYldMM0FnclRUSTQwRFJBU0JkMVFKaGo1dnVWRG82UG4rVUFkRlZ0WmZYSHloeGswcjY3ZUt0L0d1V2JkaDk3WGZMV0VMWUhkVzBWZkJPbklMUmZTaGdFOHVMa2IxZmVTS2FCUG5oS1pQWFJiYWVoVXpXbkhGSkxZPSIsIm1hYyI6IjQ4ZDNkNDVjOWQwYmE1YmQ4NzM5YmJhZWMzZGI2NTMyNDU5YjY3NzQyYzIyYTM3YjkzMjBjNjA2NzFkMGZhMGQiLCJ0YWciOiIifQ%3D%3D; ids=eyJpdiI6IlhtWC9jb25FRGhmcEw1bWxMS2t4M0E9PSIsInZhbHVlIjoielZHVm9NZ1E1eG42NGNkVld5aSsyQ2g3UUJhMDNNalI3c2NuNllxRDJaYU1hQTI0dmQ4N2M3UVd3NzdLTmpLcmFiMk9OS01NMmtQdWFFbm5SSURLcmc9PSIsIm1hYyI6Ijk3MzRjZGIxMjljYzQ1ZDU1NDgzNDljMTM4NTAyOWVkZDI4OWVjYjM5YWYxNWY1YWE0MWY4ZGE3MDg1NjVmYTQiLCJ0YWciOiIifQ%3D%3D; XSRF-TOKEN=eyJpdiI6IndIaVI4ZlNzVFhNVEREZEVVTCt6NFE9PSIsInZhbHVlIjoiRmgzeDlVK1JqdU4ya3E0a1FDcTV2VnVSZnNKRThDdWx4MnFvRTBJWVAycnBzVFBLQmNXc0pmOU91aXZzQzU3UTV0MEJTZFJuOGNHWVFlUlRxSVZvTnptRU5TZ2k4QUU3N25NRURkUXh1UnpkTnVSYnJ5ZXlBcDJEREY0V0ZIc2UiLCJtYWMiOiJiZmY1MDgwYWMwNzkxZDgyNjk0ZTA3ZTdkNGUxYTk1ZGZkNTY4OWI3MTliNWUyMWNmOTNiYTM0ODc1YWY3OGY5IiwidGFnIjoiIn0%3D; ap_session=eyJpdiI6IlhvRFlWemgyWnlNanAxeDNmOUQ2OEE9PSIsInZhbHVlIjoieXpYM2l3Mnk2Y1dXenVZcmsxdDRrQ1RYa2Jyck5xd25iNVY2KzlQV0Z2bkxEQzVQRnVmVVpac3VKQWRiK1YvdDMwNXRXblk3c25ockpiT3RKYStmeWE5dHp0VkhvWFhXRm1jbTE2V3drWnliY0xKQjVObHdBa0ZzSEV4Q2M2eTkiLCJtYWMiOiJlYWM0ZjBkMzM0NDUxNDZjNGJlMGMwYTJhMjAxYjI1ZWE0Nzc0ZDY1NWIxYzFiMjY5NjI1YjQyMDUzMGM3NDcxIiwidGFnIjoiIn0%3D; savedReferrer=eyJpdiI6InBNSjhzdk5Lc2hSeEZXTXZMZ2IvTEE9PSIsInZhbHVlIjoiRmxKQ2tRN0dNNjZqTGhKSjJzMVEzcVJZSEpJbnFqb1ZzK2NJd2dnbytWY1lod1h4NStrQW1FSnBod1BNdHlMc0ZvZDFoN01mRDVCTVdvaFF5K0Y1dTNCU2dTZzdmR0pSOVQyb1V1NjJWTkJVYW1uVDVvVXllSXV1enRBUndKZXp5bVRpSlVuQjM0Q2doU3hNZkYwUjhBPT0iLCJtYWMiOiI0MGM1ZGE0OTE1OWI4Y2VhMmU4OGZhZTIzNWJiMmJiYjQ0MTlmMmU1Njg1MzE0N2Y2YzdlZjFhZTY1MWFiNGEyIiwidGFnIjoiIn0%3D; pageCount=eyJpdiI6IlRDVFFiRWNaUGFoK3EvVVlUYUp4YXc9PSIsInZhbHVlIjoiRkVsbWxtd1JsRWptZU4wSll5em1wRUVRNHp2YU52Z0VsRmF1UDlCdTd2VjQwc2ZjOUppRzJpZG5KUkZEVEx0dCIsIm1hYyI6IjJlNGRiNWE3MjQyZjIxMGJhOWY0MWU2ZmY3ODEzNDM5NDJhOTc1YjMzNmE3N2QxNTM2YmMwMGRhNGVlZDUyZDEiLCJ0YWciOiIifQ%3D%3D; GCLB=COaQ-evzkOW4Vg; XSRF-TOKEN=eyJpdiI6InJnZmJpSWROVmt3TVdYdjVCa0FIOGc9PSIsInZhbHVlIjoiK08zaFEzT1hoMGQxVXRxS3NwcWNSalZoVmlEYm9uaHp4L2ZWWGYyTksyVlhQWkNRRXBtU3NNdFNkeVcwWHhBaXNkbENmWGpvVHhaZURPcklPWk5zWmhuS0NFcW90bHN4eFdqMDZlYmV4SjNHZDI0N2g0dnBPMXBPOFo5OXNLR0giLCJtYWMiOiI5NjUyN2Q4MDMzYTM5Mzg0ZDEzZTZlYjdmNmYyMzMyY2IxNjI3Y2E5NjQ3YzZhZTY0YjQyODFkNjM1MDBlZTA0IiwidGFnIjoiIn0%3D; ap_session=eyJpdiI6IlZzb0ZIQm0yci9tRzdkbWlZazgwTXc9PSIsInZhbHVlIjoiUHp0NzhJd1JWYmt3S2tPNW9UYzZlZHd2T1IvSi9jbW9TaGpNRHMvdkFSayt6U0I2aW9Oditzem9OdlRLeTl6cXdKYmRreTlISUsySnBid0l6V21INVp6UGVnUVJacWh3M2VsK3BYU0J3b1FyQzFPUEwraWpVMXRCY0x1am9WVWciLCJtYWMiOiIzNGEzMzUwYTYzMTNjMGRlMDUxMDg5NWQ1MTRlYWNmOGViODM1ZjQ3NTUyY2FmN2ZkN2E2YjU2NDRjNDNkYTA1IiwidGFnIjoiIn0%3D; pageCount=eyJpdiI6IjdMVnhuQjlDZU9HREhlYlpJR0QrQVE9PSIsInZhbHVlIjoiV20wTDRaSkVsZENaMXVleHByeUdENnk4cWFVRGN5R3NUUWRLM0k4WVBYci9LMUJycTNJM2ViNjZuZzB2d1pabiIsIm1hYyI6IjA1M2EzMDcyNzIwMjVlNzIwNGQ4YjdmN2Y4MjY5MjIwNWUxOTE2NzFhZmQzNDUxODM5N2MzNzI3MzVhZTViNDQiLCJ0YWciOiIifQ%3D%3D; prefs=%5BrouteSort%7Clr%5D%5BnavFilter%7CSport%5D%5BRFdiffMinrock%7C1000%5D%5BRFdiffMaxrock%7C4800%5D%5BRFstars%7C0%5D%5BRFtype%7Crock%5D%5BRFsort1%7Cpopularity%20desc%5D%5BRFsort2%7Crating%5D%5BmapX%7C-5348886%5D%5BmapY%7C4213856%5D%5BmapZoom%7C1.7%5D%5BcommentSort%7Coldest%5D',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'trailers'
    }
    API_URL = f"https://www.mountainproject.com/comments/forObject/Climb-Lib-Models-Route/{route_id}?sortOrder=oldest&showAll=true"

    response = requests.request("GET", API_URL, headers=headers, data=payload)

    # get html from response
    soup = BeautifulSoup(response.text, features='lxml')

    rows = soup.find_all('table')
    comments = []
    for row in rows:
        body = row.find('div', class_='comment-body').text.strip()
        bio = row.find('div', class_='bio')
        user_id = bio.a.get('href').split('/')[-1]
        username = bio.a.text.strip()
        # get username, hometown, user_id, ...
        hometown = bio.find('span').text.strip()

        comment = {'user_id': user_id, 'username': username,'body': body,'hometown': hometown}
        comments.append(comment)
    return comments

def get_route_data(url):
    page = urlopen(url).read()
    soup = BeautifulSoup(page, features='lxml')
    route_id = url.split('/')[-2]
    route_name = soup.find('h1').text.replace('\n', '').strip()
    route_grade = soup.find('span', class_='rateYDS').text
    ratings_data = soup.find('span', id="route-star-avg").text.replace('\n', '').strip().split(' ')
    avg_rating = float(ratings_data[1])
    num_ratings = ratings_data[3]

    # extract description
    desc_data = soup.find('table', class_='description-details')
    rows = desc_data.find_all('tr')[:3]
    climb_data = rows[0].find_all('td')[1].text.strip().split(', ')
    page_views = rows[2].find_all('td')[1].text.strip().replace('\n', '').replace('·', '').replace(' ', '').split('total')
    # extract type, height, naum_pitches, first ascenters, and page views (total / monthly)
    type_ = climb_data[0]
    height = climb_data[1]
    num_pitches = climb_data[2] if len(climb_data) == 3 else 1
    FA = rows[1].find_all('td')[1].text.strip()
    page_views_total = page_views[0]
    page_views_month = page_views[1].split('/')[0]
    # get text info
    bodies = soup.find_all('h2', class_='mt-2')
    mapping = {'Description': '', 'Permit Required': '', 'Location': '', 'Protection': ''}
    for i in range(len(bodies)):
        mapping[bodies[i].text.strip()] = bodies[i].parent.div.text.strip()

    # use API to get comments
    comments = get_comments_on_route(route_id)
    # return data as a dictionary
    data =  {'route_id': route_id, 'route_name': route_name, 
            'route_grade': route_grade, 'avg_rating': avg_rating, 
            'num_ratings': num_ratings, 'type': type_, 
            'height': height, 'num_pitches': num_pitches, 
            'FA': FA, 'page_views_total': page_views_total, 
            'page_views_month': page_views_month, 'route_comments': comments}
    data.update(mapping)

    return data


if __name__ == '__main__':
    # get CLASSICS_AREA as a command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--classics-area', help='The area to get classics from', default='105841134/red-river-gorge')
    args = parser.parse_args()
    CLASSICS_AREA = args.classics_area
    AREA_NAME = CLASSICS_AREA.split('/')[-1]
    # get all routes from a given area
    url = 'https://www.mountainproject.com/area/classics/' + CLASSICS_AREA
    climb_urls = get_classics_from_area(url)
    # get data from each route
    data = []
    for i, url in enumerate(climb_urls):
        print(f'Getting data from route {i} of {len(climb_urls)}')
        data.append(get_route_data(url))

    df = pd.DataFrame(data)
    df.to_csv(f'data/routes-{AREA_NAME}.csv')

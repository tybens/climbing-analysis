import requests
import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--classics-area', help='The area to get classics from', default='105841134/red-river-gorge')
    CLASSICS_AREA = parser.parse_args().classics_area
    AREA_NAME = CLASSICS_AREA.split('/')[-1]
    # build the url
    base_url = "https://www.mountainproject.com/api/v2/routes/"
    data_types = ['stars', 'ratings', 'ticks']
    # establish the headers
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.mountainproject.com/route/stats/106657106/edge-a-sketch',
    'Alt-Used': 'www.mountainproject.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'trailers',
    'Cookie': ''
    }


    df = pd.read_csv(f'data/routes-{AREA_NAME}.csv')
    routes = df.route_id.values
    df_ticks = pd.DataFrame()
    df_stars = pd.DataFrame()
    df_ratings = pd.DataFrame()

    for i, route in enumerate(routes):   
        print(f'Getting data from route {i} of {len(routes)}')
        for data_type in data_types:
            # iterate over the pages until data['data'] is empty and then stop
            data = []

            url = base_url + str(route) + "/" + data_type + "?per_page=250&page="
            for i in range(1, 5):
                response = requests.request("GET", url+str(i), headers=headers, data={})
                data.extend(response.json()['data'])
                if len(response.json()['data']) == 0:
                    break
            
            if data_type == 'ticks':
                new_df = pd.DataFrame(data)
                df_ticks = pd.concat([df_ticks, new_df])
            elif data_type == 'stars':
                new_df = pd.DataFrame(data)
                df_stars = pd.concat([df_stars, new_df])
            else:
                new_df = pd.DataFrame(data)
                df_ratings = pd.concat([df_ratings, new_df])

            # save the dataframes to a csv
            df_ticks.to_csv('data/ticks/ticks.csv', index=False)
            df_stars.to_csv('data/ticks/stars.csv', index=False)
            df_ratings.to_csv('data/ticks/ratings.csv', index=False)

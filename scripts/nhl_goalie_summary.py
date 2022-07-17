import requests
from flatten_json import flatten
import math
import pandas as pd

year = '20212022'

url = f'https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22timeOnIce%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={year}%20and%20seasonId%3E={year}'

r = requests.get(url)
data = r.json()['data']
count = r.json()['total']

#Count number of pages based on 100 record limit per page
pages = math.ceil(count/100)

dic_flattened = []
    
for i in range(pages):
    print(i*100)
    url_paged = f'https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22timeOnIce%22,%22direction%22:%22DESC%22%7D%5D&start={i*100}&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={year}%20and%20seasonId%3E={year}'
    r = requests.get(url_paged)
    data = r.json()['data']
    for d in data:
        dic_flattened.append(flatten(d))
        
df = pd.DataFrame(dic_flattened)
df.to_csv('2021-2022_NHLcom_Goalie_Summary.csv',index=False)

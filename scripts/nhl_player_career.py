import requests
import math
from flatten_json import flatten
import pandas as pd
import time as t

year = '20212022'

url = f'https://api.nhle.com/stats/rest/en/skater/shootout?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22skaterFullName%22,%22direction%22:%22ASC_CI%22%7D%5D&start=0&limit=100&factCayenneExp=&cayenneExp=gameTypeId=2%20and%20seasonId%3C={year}%20and%20seasonId%3E={year}'

r = requests.get(url)
count = r.json()['total']
print(count)
#Count number of pages based on 100 record limit per page
pages = math.ceil(count/100)
players = {}
for i in range(pages):
    print(i*100)
    url_paged = f'https://api.nhle.com/stats/rest/en/skater/shootout?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22skaterFullName%22,%22direction%22:%22ASC_CI%22%7D%5D&start={i*100}&limit=100&factCayenneExp=&cayenneExp=gameTypeId=2%20and%20seasonId%3C={year}%20and%20seasonId%3E={year}'
    r = requests.get(url_paged)
    data = r.json()['data']
    
    for d in data:
        players[d['playerId']] = d['skaterFullName']

print('Dictionary of players created!')

player_info = [['Id','Player','Birth Date','Birth City','Birth State/Province','Birth Country','Height','Weight','Rookie','GP','Goals','Assists','Points']]
c = 1

#Loop though every player that played at least 1 game
for key, value in players.items():
    print(f'{c}. {value} added to list')
    t.sleep(0.25)
    url = f'https://statsapi.web.nhl.com/api/v1/people/{key}?expand=person.stats&stats=careerRegularSeason'
    r = requests.get(url)
    data = r.json()['people'][0]['stats'][0]['splits'][0]['stat']
    bio = r.json()['people'][0]
    birthdate = bio.get('birthDate')
    rookie = bio.get('rookie')
    birthcity = bio.get('birthCity')
    birthstate = bio.get('birthStateProvince')
    birthcountry = bio.get('birthCountry')
    height = bio.get('height')
    weight = bio.get('weight')
    player_info.append([key,value,birthdate,birthcity,birthstate,birthcountry,height,weight,rookie,data['games'],data['goals'],data['assists'],data['points']])
    c += 1          

df = pd.DataFrame(player_info).T.set_index(0).T

df.to_csv('2021-2022_NHLcom_Player_Career.csv',index=False,encoding='utf-8-sig')

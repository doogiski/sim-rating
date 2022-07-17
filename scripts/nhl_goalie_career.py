import requests
import math
import pandas as pd
import time as t

year = '20212022'

url = f'https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22%3A%22playerId%22%2C%22direction%22%3A%22ASC%22%7D%5D&start=0&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={year}%20and%20seasonId%3E={year}'

r = requests.get(url)
count = r.json()['total']

#Count number of pages based on 100 record limit per page
pages = math.ceil(count/100)

players = {}
for i in range(pages):
    print(i*100)
    url_paged = f'https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22%3A%22playerId%22%2C%22direction%22%3A%22ASC%22%7D%5D&start={i*100}&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={year}%20and%20seasonId%3E={year}'
    r = requests.get(url_paged)
    data = r.json()['data']
    for d in data:
        players[d['playerId']] = d['goalieFullName']

print(f'{len(players)} players added to dictionary!')

player_info = [['Id','goalieFullName','Birthday','City','State/Province','Country','Height','Weight','Rookie','GP_season','TOI(minutes)_season','Wins_season','GAA_season','SV%_season','Saves_season','GP_playoffs','TOI(minutes)_playoffs','Wins_playoffs','GAA_playoffs','SV%_playoffs','Saves_playoffs']]
c = 1
for key, value in players.items():
    print(f'{c}. {value} added to list')
    t.sleep(0.25)
    url = f'https://statsapi.web.nhl.com/api/v1/people/{key}?expand=person.stats&stats=careerRegularSeason,careerPlayoffs'
    r = requests.get(url)
    data_r = r.json()['people'][0]['stats'][0]['splits'][0]['stat']
    bio = r.json()['people'][0]
    birthdate = bio['birthDate']
    rookie = bio['rookie']
    try:
        birthcity = bio['birthCity']
    except:
        birthcity = '-'
    try:
        birthstate = bio['birthStateProvince']
    except:
        birthstate = '-'
    birthcountry = bio['birthCountry']
    height = bio['height']
    weight = bio['weight']
    #Try for playoff data
    try:
        data_p = r.json()['people'][0]['stats'][1]['splits'][0]['stat']
        games_p = data_p['games']
        wins_p = data_p['wins']
        gaa_p = data_p['goalAgainstAverage']
        sv_p = data_p['savePercentage']
        saves_p = data_p['saves']
        hp = data_p['timeOnIce']
        hrsp, mnp = hp.split(':')
        minutes_p = (int(hrsp) * 60) + int(mnp) 
    except IndexError:
        games_p = 0
        wins_p = 0
        gaa_p = 0
        sv_p = 0
        saves_p = 0
        minutes_p = 0
    
    h = data_r['timeOnIce']
    hrs, mn = h.split(':')
    minutes = (int(hrs) * 60) + int(mn)
        
    player_info.append([key,value,birthdate,birthcity,birthstate,birthcountry,height,weight,rookie,data_r['games'],minutes,data_r['wins'],data_r['goalAgainstAverage'],data_r['savePercentage'],data_r['saves'],games_p,wins_p,gaa_p,sv_p,saves_p,minutes_p])
    c += 1          

df = pd.DataFrame(player_info).T.set_index(0).T

df.to_csv('2021-2022_NHLcom_Goalie_Career.csv',index=False)

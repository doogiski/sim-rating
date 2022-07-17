import requests
from bs4 import BeautifulSoup
import pandas as pd
import time as t

year1 = '1999'
year2 = '2000'

appended_data = []
#Loop through years starting 23 years ago
for i in range(23):
    t.sleep(2)
    year = f'{i+year1}-{i+year2}'
    print(year)
    url = f'https://www.eliteprospects.com/league/nhl/team-captaincy/{year}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    caps = []
    ass = []
    #Get Table
    table = soup.find_all('div', attrs = {'class','table-wizard'})[1]
    for row in table.find_all('tr'):
        teams = row.find_all('a')
        #Create Captains List
        for i in teams[1:2]:
            caps.append(i.text)
        #Create Assistant Captains List
        for j in teams[2:]:
            ass.append(j.text)

    captains = [[player,1,0] for player in caps]
    assistants = [[player,0,1] for player in ass]

    appended_data.extend(captains)
    appended_data.extend(assistants)

df = pd.DataFrame(appended_data,columns=['Player','Captaincy','Assistant'])
df_agg = df.groupby('Player')[['Captaincy','Assistant']].sum().reset_index()        

df_agg.to_csv('2021-2022-elite_prospects-captaincy.csv',index=False)

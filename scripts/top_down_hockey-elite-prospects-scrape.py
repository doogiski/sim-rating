import TopDownHockey_Scraper.TopDownHockey_EliteProspects_Scraper as tdhepscrape

year = '2021-2022'
#Grab all goalies
output = tdhepscrape.get_goalies("ahl", year)

#Grab all skaters
output = tdhepscrape.get_skaters("ahl", year)

io = tdhepscrape.add_player_information(output)

io.to_csv("ahl_goalies.csv",index=False)

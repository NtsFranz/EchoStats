# Echopedia
Scripts to scrape the ESL and VRML sites and upload the data to the Wiki or to a Firebase db

## WIKI upload process
 - `Scrape_ESL_VRML.py` -> `scrapeESLCups()`
   - creates cups json files as well as simple data in teams.json
 - `Scrape_ESL_VRML.py` -> `scrapeESLTeams()`
   - scrapes each team page on the esl website and adds more info to teams.json
 - `Scrape_ESL_VRML.py` -> `scrapeESLMatchPages()`
   - scrapes each match page and gets info about which players played and sets it to teams.json and players.json
 - `Scrape_ESL_VRML.py` -> `add_players_matches()`
   - reads cup json files and adds data to matches.json, teams.json, and players.json
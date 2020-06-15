import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from pyquery import PyQuery as pq
from pathlib import Path
from google.cloud import storage
import os
import datetime
import json


#################
# Init Firestore
#################
project_id="ignitevr-echostats"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ignitevr-echostats-firebase-adminsdk-nzhes-c287edff87.json"

# Use the application default credentials
#cred = credentials.Certificate("ignitevr-echostats-firebase-adminsdk-nzhes-c287edff87.json")
cred = credentials.Certificate("ignitevr-echostats-9e1d8f70c8a0.json")
firebase_admin.initialize_app(cred, { 'projectId': project_id })
#firebase_admin.get_app()


db = firestore.client()


##################
# Actually scrape
##################

baseURL = 'https://vrmasterleague.com'

team_name_set = set([])


def scrapeTeams():
    return # DON'T CALL THIS BECAUSE THE DATA ON THE WEBSITE IS NOW NO LONGER THERE
    teams = { "vrml_preseason": [], "vrml_season_1": [] }
    matches = { "vrml_preseason": [], "vrml_season_1": [] }
    
    
    series = [
        {
            "name": "vrml_preseason", 
            "url": "https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnJNSzVPMG9XcTlLdz090"
        }, 
        {
            "name": "vrml_season_1", 
            "url": "https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090"
        }
    ]
    
    for season in series:
        page = pq(season['url'])
        for teamHTML in page('.standings_information > .vrml_table_container > .vrml_table > tbody > tr'):
            team_matches_temp = []
            team_pq = pq(teamHTML)
            team = {}
            team['team_name'] = team_pq('.team_name').text()
            team['team_page'] = baseURL + team_pq('.team_link').attr('href')
            team['team_logo'] = baseURL + team_pq('.team_logo').attr('src')
            team['division'] = team_pq('.div_cell > img').attr('title')
            team['division_logo'] = baseURL + team_pq('.div_cell > img').attr('src')
            team['rank'] = team_pq('.pos_cell').text()
            team['region'] = team_pq('.group_cell > img').attr('title')
            team['region_logo'] = baseURL + team_pq('.group_cell > img').attr('src')
            team['games_played'] = team_pq('.gp_cell').text()
            team['wins'] = team_pq('.win_cell').text()
            team['losses'] = team_pq('.loss_cell').text()
            team['points'] = team_pq('.pts_cell').text()
            team['mmr'] = team_pq('.mmr_cell').text()
            
            default_team_page = pq(team['team_page'])
            
            # go to the right season's page
            for season_option in default_team_page('.team_season_switcher > option'):
                opt = pq(season_option)
                if opt.attr('value') == "Pre-season - 2019 (history)" and season['name'] == "vrml_preseason":
                    team['team_page'] = baseURL + "/EchoArena/Teams/" + opt.attr('value')
                    break
                if opt.attr('value') == "Season 1 - 2020" and season['name'] == "vrml_season_1":
                    team['team_page'] = baseURL + "/EchoArena/Teams/" + opt.attr('value')
                    break
            
            # actually go to the team page for the correct season and get more stats from there
            team_page = pq(team['team_page'])
            
            roster = []
            for p in team_page('.player_name'):
                roster.append(pq(p).text())
            team['roster'] = roster
            
            
            team_name_set.add(team['team_page'])
            
            teams[season['name']].append(team)
            
            # scrape the match history on the team page
            for matchHTML in team_page('.teams_recent_matches_table > tbody > tr'):
                match_pq = pq(matchHTML)
                match = {}
                match['match_id'] = match_pq('.match-page-info > a').attr('href').split('/')[3]
                match['time'] = match_pq('.date_recent_cell').text()
                match['home_team_name'] = match_pq('.home_team_cell').text()
                match['home_team_score'] = match_pq('.score_cell').text().split(' ')[0]
                match['away_team_score'] = match_pq('.score_cell').text().split(' ')[2]
                match['away_team_name'] = match_pq('.away_team_cell').text()
                match['away_team_name'] = match_pq('.away_team_cell').text()
                match['video_url'] = match_pq('.match-video-url-wrapper').attr('href')
                
                caster_cells = [i for i in match_pq('.caster-vod-cell').items()]
                casters = []
                for e in pq(caster_cells[1])('.caster-name').items():
                    casters.append(e.text())
                match['casters'] = casters
                
                cameramen = []
                for e in pq(caster_cells[2])('.caster-name').items():
                    cameramen.append(e.text())
                match['cameramen'] = cameramen
                match['match_page'] = baseURL + match_pq('.match-page-info > a').attr('href')
                match['challenge'] = match_pq('.date_recent_cell > img').hasClass('challenge_icon')
                team_matches_temp.append(match)
                matches[season['name']].append(match)
                
            # Insert into DB
            insertIntoDB([team], "series/"+season['name']+'/teams', 'team_name')
            insertIntoDB(team_matches_temp, "series/"+season['name']+'/matches', 'match_id')



def scrapePlayers():
    return # DON'T CALL THIS BECAUSE THE DATA ON THE WEBSITE IS NOW NO LONGER THERE
    players = []
    VRML_URL = "https://vrmasterleague.com/EchoArena/Players/List/"

    page = pq(VRML_URL)
    numPlayers = int(page('.players-list-header-count').text()[20:23])

    for i in range(0,int(numPlayers/100)+1):
        page = pq(VRML_URL+"?posMin="+str(i*100+1))

        for playerHTML in page('.vrml_table_row'):
            player_pq = pq(playerHTML)
            player = {}
            player['player_name'] = player_pq('.player_cell > a > span').text()
            player['player_page'] = baseURL + player_pq('.player_cell > a').attr('href')
            player['player_logo'] = baseURL + player_pq('.player_cell > a > img').attr('src')
            player['team_name'] = player_pq('.team_cell > a > span').text()
            player['team_page'] = baseURL + player_pq('.team_cell > a').attr('href')
            player['team_logo'] = baseURL + player_pq('.team_cell > a > img').attr('src')
            nat_img_cell = player_pq('.nationality_cell > img')
            if nat_img_cell:
                player['nationality'] = nat_img_cell.attr('title')
                player['nationality_logo'] = baseURL + nat_img_cell.attr('src')
            else:
                player['nationality'] = None
                player['nationality_logo'] = None
                

            players.append(player)

    # Insert into DB
    insertIntoDB(players, 'players', 'player_name')
    
def writeImage(url, filename):
    with open(filename, 'wb') as outfile:
        r = requests.get(url, stream=True)
        for block in r.iter_content(1024):
            if not block:
                break
            outfile.write(block)
        print(filename)

# downloads the image urls in the firebase database and stores them in firebase storage
def downloadImages():
    Path("images/logos/teams").mkdir(parents=True, exist_ok=True)
    Path("images/logos/users").mkdir(parents=True, exist_ok=True)

    players = db.collection('players').stream()
    teams_s0 = db.collection('series/vrml_preseason/teams').stream()
    teams_s1 = db.collection('series/vrml_season_1/teams').stream()
    
    for player in players:
        # player profile picture
        fullPath = player.to_dict()['player_logo']
        fileName = fullPath[27:]
        writeImage(fullPath, fileName)
        
        # team picture
        fullPath = player.to_dict()['team_logo']
        fileName = fullPath[27:]
        writeImage(fullPath, fileName)
        
        
# uploads images from a folder structure into firebase
def uploadImages():
    client = storage.Client()
    bucket = client.get_bucket('ignitevr-echostats.appspot.com')
    
    path="images"
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    
    for f in files:
        f = f.replace('\\', '/')
        blob = bucket.blob(f)
        blob.upload_from_filename(f)
        print(f)

    
def insertIntoDB(arr_of_dict, collection_name, key_name=None):
    batch = db.batch()
    for elem in arr_of_dict:
        if key_name is None:
            doc_ref = db.collection(collection_name).document()
        else:
            doc_ref = db.collection(collection_name).document(elem[key_name])
            del elem[key_name]
        batch.set(doc_ref, elem)
    batch.commit()
    
    
def scrapeESLPlayers():
    esl_data = {
        "cups": []
    }

    teams = {} # unique team names
    baseURL = "https://play.eslgaming.com"
    URL = "https://play.eslgaming.com/echoarena/north-america/tournaments"

    naURL = "https://api.eslgaming.com/play/v1/leagues?types=a_series,cup,esl_series,ladder,premiership,swiss&states=finished&tags=&path=/play/echoarena/north-america/&includeHidden=0&skill_levels=pro_qualifier,open,pro,major&limit.total=2000"
    euURL = "https://api.eslgaming.com/play/v1/leagues?types=a_series,cup,esl_series,ladder,premiership,swiss&states=finished&tags=&path=/play/echoarena/europe/&includeHidden=0&skill_levels=pro_qualifier,open,pro,major&limit.total=2000"

    contestantsURL = "https://api.eslgaming.com/play/v1/leagues/162327/contestants"

    r = requests.get(euURL)
    cupsPages = json.loads(r.text)
    for cup in cupsPages.items():
        pageURL = baseURL + cup[1]['uri']
        cup_data = {
            "link": pageURL,
            "teams": []
        }
        if '-registration' in pageURL:
            contestantsURL = "https://api.eslgaming.com/play/v1/leagues/" + cup[0] + "/contestants"
            r = requests.get(contestantsURL)
            contestants = json.loads(r.text)
            for c in contestants:
                cup_data['teams'].append()
                teams[c['id']] = {'team_name': c['name']}
                print(c['name'])
        
        esl_data['cups'].append(cup_data)

    for team in teams:
        teamPageURL = "https://play.eslgaming.com/team/" + str(team)
        teamPage = pq(teamPageURL)
        teams[team]['team_page'] = teamPageURL
        if teamPage('#team_logo_overlay_image').attr('src'):
            teams[team]['team_logo'] = teamPage('#team_logo_overlay_image').attr('src')
        teamDataRows = teamPage('.playerprofile_stammdaten > tr')
        for row in teamDataRows.items():
            firstcol = pq(row)('.firstcol, .lastrowfirstcol')
            if firstcol.text() == "Registered since":
                teams[team]['founded'] = datetime.datetime.strptime(firstcol.next().text(), "%d/%m/%y")
            elif "Headquarters" in firstcol.text():
                teams[team]['region'] = firstcol.next()('b').text()
        playerList = pq(teamPage('#playersheet_title').next())('tr > td > div')('a')
        players = []
        for playerElem in playerList:
            if "Show all matches" not in playerElem.text:
                players.append(playerElem.text)
        teams[team]['roster'] = players
        print("Got roster for: " + teams[team]['team_name'])

    # convert dict to array of dicts
    teamsArr = []
    for team in teams:
        teamsArr.append(teams[team])

    # insertIntoDB(teamsArr, 'series/esl_season_1/teams', 'team_name')
    return teamsArr
        

def upload_players_wiki():
    print(scrapeESLPlayers())

#scrapePlayers()
#scrapeMatches()
#scrapeTeams()
#downloadImages()
#uploadImages()
#scrapeESLPlayers()

upload_players_wiki()
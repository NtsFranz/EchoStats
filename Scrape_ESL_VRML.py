import requests
from pyquery import PyQuery as pq
from pathlib import Path
import os
import datetime
import json

baseURL = 'https://vrmasterleague.com'

team_name_set = set([])


def scrapeTeams():
    return  # DON'T CALL THIS BECAUSE THE DATA ON THE WEBSITE IS NOW NO LONGER THERE
    teams = {"vrml_preseason": [], "vrml_season_1": []}
    matches = {"vrml_preseason": [], "vrml_season_1": []}

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
            team['division_logo'] = baseURL + \
                team_pq('.div_cell > img').attr('src')
            team['rank'] = team_pq('.pos_cell').text()
            team['region'] = team_pq('.group_cell > img').attr('title')
            team['region_logo'] = baseURL + \
                team_pq('.group_cell > img').attr('src')
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
                    team['team_page'] = baseURL + \
                        "/EchoArena/Teams/" + opt.attr('value')
                    break
                if opt.attr('value') == "Season 1 - 2020" and season['name'] == "vrml_season_1":
                    team['team_page'] = baseURL + \
                        "/EchoArena/Teams/" + opt.attr('value')
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
                match['match_id'] = match_pq(
                    '.match-page-info > a').attr('href').split('/')[3]
                match['time'] = match_pq('.date_recent_cell').text()
                match['home_team_name'] = match_pq('.home_team_cell').text()
                match['home_team_score'] = match_pq(
                    '.score_cell').text().split(' ')[0]
                match['away_team_score'] = match_pq(
                    '.score_cell').text().split(' ')[2]
                match['away_team_name'] = match_pq('.away_team_cell').text()
                match['away_team_name'] = match_pq('.away_team_cell').text()
                match['video_url'] = match_pq(
                    '.match-video-url-wrapper').attr('href')

                caster_cells = [i for i in match_pq(
                    '.caster-vod-cell').items()]
                casters = []
                for e in pq(caster_cells[1])('.caster-name').items():
                    casters.append(e.text())
                match['casters'] = casters

                cameramen = []
                for e in pq(caster_cells[2])('.caster-name').items():
                    cameramen.append(e.text())
                match['cameramen'] = cameramen
                match['match_page'] = baseURL + \
                    match_pq('.match-page-info > a').attr('href')
                match['challenge'] = match_pq(
                    '.date_recent_cell > img').hasClass('challenge_icon')
                team_matches_temp.append(match)
                matches[season['name']].append(match)

            # Insert into DB
            insertIntoDB([team], "series/"+season['name'] +
                         '/teams', 'team_name')
            insertIntoDB(team_matches_temp, "series/" +
                         season['name']+'/matches', 'match_id')


def scrapePlayers():
    return  # DON'T CALL THIS BECAUSE THE DATA ON THE WEBSITE IS NOW NO LONGER THERE
    players = []
    VRML_URL = "https://vrmasterleague.com/EchoArena/Players/List/"

    page = pq(VRML_URL)
    numPlayers = int(page('.players-list-header-count').text()[20:23])

    for i in range(0, int(numPlayers/100)+1):
        page = pq(VRML_URL+"?posMin="+str(i*100+1))

        for playerHTML in page('.vrml_table_row'):
            player_pq = pq(playerHTML)
            player = {}
            player['player_name'] = player_pq('.player_cell > a > span').text()
            player['player_page'] = baseURL + \
                player_pq('.player_cell > a').attr('href')
            player['player_logo'] = baseURL + \
                player_pq('.player_cell > a > img').attr('src')
            player['team_name'] = player_pq('.team_cell > a > span').text()
            player['team_page'] = baseURL + \
                player_pq('.team_cell > a').attr('href')
            player['team_logo'] = baseURL + \
                player_pq('.team_cell > a > img').attr('src')
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

    path = "images"
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

# Gets all VRCL matches from na/eu using API and returns the result as a dict


def scrapeESLCups():
    esl_data = {
        "cups": [],
        "teams": {}
    }

    teams = {}  # unique team names
    baseURL = "https://play.eslgaming.com"
    URL = "https://play.eslgaming.com/echoarena/north-america/tournaments"

    regionURLS_VRCL = ["https://api.eslgaming.com/play/v1/leagues?types=a_series,cup,esl_series,ladder,premiership,swiss&states=finished&tags=&path=/play/echoarena/north-america/&includeHidden=0&skill_levels=pro_qualifier,open,pro,major&limit.total=5000",
                       "https://api.eslgaming.com/play/v1/leagues?types=a_series,cup,esl_series,ladder,premiership,swiss&states=finished&tags=&path=/play/echoarena/europe/&includeHidden=0&skill_levels=pro_qualifier,open,pro,major&limit.total=5000"]

    regionURLS_VRL = [
        "https://api.eslgaming.com/play/v1/leagues?types=swiss&states=finished&tags=vrlechoarena-na-portal&path=/play/&includeHidden=0&skill_levels=major&limit.total=40000",
        "https://api.eslgaming.com/play/v1/leagues?types=swiss&states=finished&tags=vrlechoarena-eu-portal&path=/play/&includeHidden=0&skill_levels=major&limit.total=40000"]

    for url in regionURLS_VRL:
        r = requests.get(url)
        cups = json.loads(r.text)
        for cupItem in cups.items():
            cup = cupItem[1]

            if '2019-' not in cup['uri']:
                continue

            pageURL = baseURL + cup['uri']
            cup_data = {
                "id": cup['id'],
                "link": pageURL,
                "name": cup['name']['normal'],
                "date": cup['timeline']['inProgress']['begin'] if len(cup['timeline']) > 0 else "n/a",
                "teams": [],
                "matches": []
            }

            # Get participating teams
            contestantsURL = "https://api.eslgaming.com/play/v1/leagues/" + \
                str(cup['id']) + "/contestants"
            r = requests.get(contestantsURL)
            print(contestantsURL)
            contestants = json.loads(r.text)
            for c in contestants:
                cup_data['teams'].append({
                    "id": c['id'],
                    "team_name": c['name']
                })
                teams[c['id']] = {'team_name': c['name']}

            # get matches
            matchesURL = "https://api.eslgaming.com/play/v1/leagues/" + \
                str(cup['id']) + "/matches"
            r = requests.get(matchesURL)
            print(matchesURL)
            matches = json.loads(r.text)
            for m in matches:
                cup_data['matches'].append({
                    "id": m['id'],
                    "teams": [
                        {
                            "id": m['contestants'][0]['team']['id'],
                            "team_name": m['contestants'][0]['team']['name'],
                            "team_logo": m['contestants'][0]['team']['logo'],
                            "score": m['result']['score'][m['contestants'][0]['team']['id'] if m['contestants'][0]['team']['id'] is not None else "0"]
                        },
                        {
                            "id": m['contestants'][1]['team']['id'],
                            "team_name": m['contestants'][1]['team']['name'],
                            "team_logo": m['contestants'][1]['team']['logo'],
                            "score": m['result']['score'][m['contestants'][1]['team']['id'] if m['contestants'][1]['team']['id'] is not None else "0"]
                        }
                    ],
                    "match_time": m['beginAt']
                })

            esl_data['cups'].append(cup_data)
    esl_data['teams'] = teams

    with open('data/VRL_S3_cups.json', 'w') as outfile:
        json.dump(esl_data, outfile)

# Gets all teams and players on teams from ESL site
# gets teams from json file, exports to json file


def get_esl_players_from_team_list():
    with open('data/VRL_S3_cups.json', 'r+') as f:
        esl_data = json.load(f)
        f.seek(0)

        for teamItem in esl_data['teams'].items():
            team = teamItem[1]
            teamPageURL = "https://play.eslgaming.com/team/" + str(teamItem[0])
            teamPage = pq(teamPageURL)
            print(teamPageURL)
            team['team_page'] = teamPageURL
            if teamPage('#team_logo_overlay_image').attr('src'):
                team['team_logo'] = teamPage(
                    '#team_logo_overlay_image').attr('src')
            teamDataRows = teamPage('.playerprofile_stammdaten > tr')
            for row in teamDataRows.items():
                firstcol = pq(row)('.firstcol, .lastrowfirstcol')
                if firstcol.text() == "Registered since":
                    #team['founded'] = datetime.datetime.strptime(firstcol.next().text(), "%d/%m/%y").strftime('%Y-%m-%d %H:%M:%S')
                    team['founded'] = firstcol.next().text()
                elif "Headquarters" in firstcol.text():
                    team['region'] = firstcol.next()('b').text()
            playerList = pq(teamPage('#playersheet_title').next())(
                'tr > td > div')('a')
            players = []
            for playerElem in playerList:
                if playerElem.text is not None and "Show all matches" not in playerElem.text:
                    p = {
                        "id": pq(playerElem).attr('href').split('/')[2],
                        "name": playerElem.text,
                        "player_page": "https://play.eslgaming.com" + pq(playerElem).attr('href')
                    }
                    players.append(p)
            team['roster'] = players

        json.dump(esl_data, f)
        f.truncate()

# reads cup json files and adds data to teams.json and players.json
def add_players():
    if os.path.exists('data/players.json'):
        with open('data/players.json', 'r') as f:
            players = json.load(f)
    else:
        players = {}

    if os.path.exists('data/teams.json'):
        with open('data/teams.json', 'r') as f:
            teams = json.load(f)
    else:
        teams = {}

    files = {
        'vrcl_s1': 'data/VRCL_S1_cups.json',
        'vrl_s2': 'data/VRL_S2_cups.json',
        'vrl_s3': 'data/VRL_S3_cups.json',
        'vrml_preseason': 'data/VRML_preseason.json',
        'vrml_s1': 'data/VRML_S1.json',
        'vrml_s2': 'data/VRML_S2.json'
    }

    for file in files.items():
        with open(file[1], 'r') as f:
            esl_data = json.load(f)

        for team in esl_data['teams'].items():
            for player in team[1]['roster']:
                if player['name'] not in players:
                    players[player['name']] = {}
                p = players[player['name']]
                p['player_name'] = player['name']
                p['esl_player_page'] = player['player_page']
                p['esl_player_id'] = player['id']

                if 'teams' not in p:
                    p['teams'] = []

                team_name = team[1]['team_name']
                if team_name not in p['teams']:
                    p['teams'].append(team_name)

                if team_name not in teams:
                    teams[team_name] = {}
                t = teams[team_name]

                t['esl_team_id'] = team[0]
                t['esl_team_page'] = team[1]['team_page']
                t['esl_team_logo'] = team[1]['team_logo']
                t['esl_founded'] = team[1]['team_logo']
                t['esl_region'] = team[1]['team_logo']

                # add the roster to the current season
                if 'series' not in t:
                    t['series'] = {}
                if file[0] not in t['series']:
                    t['series'][file[0]] = {}
                t['series'][file[0]]['roster'] = [elem['name'] for elem in team[1]['roster']]

    with open('data/players.json', 'w') as f:
        json.dump(players, f)
    
    with open('data/teams.json', 'w') as f:
        json.dump(teams, f)


# scrapePlayers()
# scrapeMatches()
# scrapeTeams()
# downloadImages()
# uploadImages()

# scrapeESLCups()
# get_esl_players_from_team_list()
add_players()
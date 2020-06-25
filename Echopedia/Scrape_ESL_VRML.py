import requests
from pyquery import PyQuery as pq
from pathlib import Path
import os
import datetime
import json

from WikiCommon import *

baseURL = 'https://vrmasterleague.com'

team_name_set = set([])


def scrapeTeams():
    with open('data/teams.json', 'r') as f:
        teams = json.load(f)

    matches = {}

    series = [
        {
            "name": "vrml_preseason",
            "url": "https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnJNSzVPMG9XcTlLdz090"
        },
        {
            "name": "vrml_season_1",
            "url": "https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090"
        },
        {
            "name": "vrml_season_2",
            "url": "https://vrmasterleague.com/EchoArena/Standings/d3JZU1F5WlVraGc90"
        }
    ]

    for season in series:
        # load the series rankings
        page = pq(season['url'])
        print(season['url'])
        for teamHTML in page('.standings_information > .vrml_table_container > .vrml_table > tbody > tr'):
            team_matches_temp = []
            team_pq = pq(teamHTML)
            team = {}
            team['team_name'] = team_pq('.team_name').text()
            if team['team_name'] is None or team['team_name'] == '':
                print("skipping team. No team name.")
                continue
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

            # load the team page
            default_team_page = pq(team['team_page'])
            print(team['team_page'])

            # go to the right season's page
            for season_option in default_team_page('.team_season_switcher > option'):
                opt = pq(season_option)
                if opt.text() == "Pre-season - 2019 (history)" and season['name'] == "vrml_preseason":
                    team['team_page'] = baseURL + \
                        "/EchoArena/Teams/" + opt.attr('value')
                    break
                if opt.text() == "Season 1 - 2020 (history)" and season['name'] == "vrml_season_1":
                    team['team_page'] = baseURL + \
                        "/EchoArena/Teams/" + opt.attr('value')
                    break
                if opt.text() == "Season 2 - 2020" and season['name'] == "vrml_season_2":
                    team['team_page'] = baseURL + \
                        "/EchoArena/Teams/" + opt.attr('value')
                    break

            # actually go to the team page for the correct season and get more stats from there
            team_page = pq(team['team_page'])

            roster = []
            if season['name'] == "vrml_season_2":
                past_roster = team_page('.players_container .player_name')
            else:
                past_roster = team_page(
                    '.teams_roster_season_container .player_name')

            for p in past_roster:
                roster.append(pq(p).text())
            team['roster'] = roster

            team_name_set.add(team['team_page'])

            # scrape the match history on the team page
            season_matches = []
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

                season_matches.append(match)

            matches[season['name']] = season_matches

            # start adding this stuff to teams.json
            if team['team_name'] not in teams:
                teams[team['team_name']] = {}
            t = teams[team['team_name']]

            team_id = str(team['team_page'].split('/')[-1])
            # check if this team name was already used by a different team id
            if 'vrml_team_id' in t and t['vrml_team_id'] != team_id:
                print("Conflicting team names.")
            t['vrml_team_id'] = team_id
            t['vrml_team_page'] = team['team_page']
            t['vrml_team_logo'] = team['team_logo']
            t['vrml_region'] = team['region']
            t['vrml_region_logo'] = team['region_logo']

            if 'series' not in t:
                t['series'] = {}
            if season['name'] not in t['series']:
                t['series'][season['name']] = {}
            teams_season = t['series'][season['name']]
            teams_season['matches'] = season_matches
            teams_season['division'] = team['division']
            teams_season['division_logo'] = team['division_logo']
            teams_season['rank'] = team['rank']
            teams_season['games_played'] = team['games_played']
            teams_season['wins'] = team['wins']
            teams_season['losses'] = team['losses']
            teams_season['points'] = team['points']
            teams_season['mmr'] = team['mmr']
            teams_season['roster'] = team['roster']

            # Insert into DB
            # insertIntoDB([team], "series/"+season['name'] +
            #              '/teams', 'team_name')
            # insertIntoDB(team_matches_temp, "series/" +
            #              season['name']+'/matches', 'match_id')

    with open('data/teams.json', 'w') as f:
        json.dump(teams, f)


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


# Gets all VRCL/VRL matches from na/eu using API and returns the result as a dict
# resets data added to cup json files
def scrapeESLCups():

    if os.path.exists('data/teams.json'):
        with open('data/teams.json', 'r') as f:
            teams = json.load(f)
    else:
        teams = {}

    for season in seasons_data.items():
        if season[1]['api_type'] != 'esl':
            continue

        if os.path.exists(season[1]['file']):
            with open(season[1]['file'], 'r') as f:
                esl_data = json.load(f)
        else:
            esl_data = {}

        season_teams = {}  # list of all teams in this season

        baseURL = "https://play.eslgaming.com"

        for url in season[1]['api_urls'].items():
            r = requests.get(url[1])
            cups = json.loads(r.text)
            for cupItem in cups.items():
                cup = cupItem[1]

                # skip s3 in s2
                if '2019-' in cup['uri'] and season[0] == 'vrl_s2':
                    continue

                # skip s2 in s3
                if '2019-' not in cup['uri'] and season[0] == 'vrl_s3':
                    continue

                pageURL = baseURL + cup['uri']
                cup_data = {
                    "id": cup['id'],
                    "link": pageURL,
                    "name": cup['name']['normal'],
                    "date": cup['timeline']['inProgress']['begin'] if len(cup['timeline']) > 0 else "n/a",
                    "teams": {},
                    "matches": []
                }

                # Get participating teams
                contestantsURL = "https://api.eslgaming.com/play/v1/leagues/" + \
                    str(cup['id']) + "/contestants"
                r = requests.get(contestantsURL)
                print(contestantsURL)
                contestants = json.loads(r.text)
                for c in contestants:

                    if c['name'] not in cup_data['teams']:
                        cup_data['teams'][c['name']] = {}
                    cup_data['teams'][c['name']]['id'] = c['id']

                    if c['name'] not in teams:
                        teams[c['name']] = {}
                    teams[c['name']]['esl_team_id'] = c['id']

                    if c['name'] not in season_teams:
                        season_teams[c['name']] = {}
                    season_teams[c['name']]['esl_team_id'] = c['id']

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

                if 'cups' not in esl_data:
                    esl_data['cups'] = []
                esl_data['cups'].append(cup_data)

        esl_data['teams'] = season_teams

        with open(season[1]['file'], 'w') as outfile:
            json.dump(esl_data, outfile)

    with open('data/teams.json', 'w') as f:
        json.dump(teams, f)


# Gets all teams and players on teams from ESL site
# gets teams from json file, exports to json file
def scrapeESLTeams():

    with open('data/teams.json', 'r') as f:
        teams = json.load(f)

    for teamItem in teams.items():
        # skip teams that are not from ESL
        if 'esl_team_id' not in teamItem[1]:
            continue

        team = teamItem[1]
        teamPageURL = "https://play.eslgaming.com/team/" + \
            str(team['esl_team_id'])
        teamPage = pq(teamPageURL)
        print(teamPageURL)
        team['esl_team_page'] = teamPageURL
        if teamPage('#team_logo_overlay_image').attr('src'):
            team['esl_team_logo'] = teamPage(
                '#team_logo_overlay_image').attr('src')
        teamDataRows = teamPage('.playerprofile_stammdaten > tr')
        for row in teamDataRows.items():
            firstcol = pq(row)('.firstcol, .lastrowfirstcol')
            if firstcol.text() == "Registered since":
                #team['founded'] = datetime.datetime.strptime(firstcol.next().text(), "%d/%m/%y").strftime('%Y-%m-%d %H:%M:%S')
                team['esl_founded'] = firstcol.next().text()
            elif "Headquarters" in firstcol.text():
                team['esl_region'] = firstcol.next()('b').text()
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

    with open('data/teams.json', 'w') as f:
        json.dump(teams, f)


def scrapeMatchPages():

    if os.path.exists('data/players.json'):
        with open('data/players.json', 'r') as f:
            players = json.load(f)
    else:
        players = {}

    for season in seasons_data.items():
        if season[1]['api_type'] != 'esl':
            continue

        with open(season[1]['file'], 'r') as f:
            cups = json.load(f)

        # loop through all the cups in this season
        for cup in cups['cups']:
            # loop through all the matches in this cup
            for match in cup['matches']:
                # get the match page
                match['match_page'] = cup['link'] + 'match/' + str(match['id'])
                matchPage = pq(match['match_page'])
                print(match['match_page'])

                # scrape the match page
                # loop through the two teams in the match
                for team in match['teams']:
                    # ignore completely deleted teams
                    if team['id'] is None:
                        continue

                    # get the team name even for deleted teams
                    team['team_page'] = cup['link'] + 'team/' + str(team['id'])
                    new_team_name = matchPage(
                        'a[href*="' + 'team/' + str(team['id']) + '"]').text()
                    if new_team_name != team['team_name'] and team['team_name'] != "Deleted account":
                        print("Different team name")
                    team['team_name'] = new_team_name

                    # find the player list part of the page
                    if matchPage('h4:contains("'+team['team_name']+'")'):
                        team['roster'] = []
                        players_box = matchPage(
                            'h4:contains("'+team['team_name']+'")').nextAll('.flex-container').eq(0)
                        esl_players = players_box.children()
                        for player in esl_players:
                            player = pq(player)
                            player_data = {
                                'player_name': player('a').eq(0).text(),
                                'esl_player_page': baseURL + player('a').attr('href'),
                                'esl_player_id': int(player('a').attr('href').split('/')[-2]),
                                'esl_player_logo': player('a img').attr('src')
                            }
                            team['roster'].append(player_data)

                            if player_data['player_name'] not in players:
                                players[player_data['player_name']] = {}
                            p = players[player_data['player_name']]
                            p['player_name'] = player_data['player_name']
                            p['esl_player_page'] = player_data['esl_player_page']
                            p['esl_player_id'] = player_data['esl_player_id']
                            p['esl_player_logo'] = player_data['esl_player_logo']

        with open(season[1]['file'], 'w') as f:
            json.dump(cups, f)

    with open('data/players.json', 'w') as f:
        json.dump(players, f)


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

    for file in seasons_data.items():
        with open(file[0]['file'], 'r') as f:
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
                t['series'][file[0]]['roster'] = [elem['name']
                                                  for elem in team[1]['roster']]

    with open('data/players.json', 'w') as f:
        json.dump(players, f)

    with open('data/teams.json', 'w') as f:
        json.dump(teams, f)


# scrapePlayers()
# scrapeMatches()
# scrapeTeams()
# downloadImages()
# uploadImages()

scrapeESLCups()
# scrapeESLTeams()
# scrapeMatchPages()

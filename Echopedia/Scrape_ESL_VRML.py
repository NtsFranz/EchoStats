import requests
from pyquery import PyQuery as pq
from pathlib import Path
import os
import datetime
import json

from WikiCommon import *

baseURL = 'https://vrmasterleague.com'
baseURLESL = 'https://play.eslgaming.com'


def scrapeVRMLTeams():
    with open('data/teams.json', 'r') as f:
        teams = json.load(f)

    with open('data/matches.json', 'r') as f:
        matches = json.load(f)

    # loop through the seasons known
    for season_id, season in seasons_data.items():

        # skip esl seasons
        if season['api_type'] != 'vrml':
            continue

        # load the series rankings to get all the team names
        page = pq(season['standings_url'])
        print(season['standings_url'])

        # loop through the teams on this page
        for teamHTML in page('.standings_information > .vrml_table_container > .vrml_table > tbody > tr'):
            team_matches_temp = []
            team_pq = pq(teamHTML)
            team = {}

            # get the info available on the single row in the rankings
            team['team_name'] = team_pq('.team_name').text()
            if team['team_name'] is None or team['team_name'] == '':
                print("skipping team. No team name.")
                continue

            # if the team name has changed save the old one, but use the new one
            if ' (aka ' in team['team_name']:
                team['old_team_name'] = team['team_name'].split(' (aka ')[0]
                team['team_name'] = team['team_name'].split(' (aka ')[1][:-1]
                print('old name: ' + team['old_team_name'])
                print('new name: ' + team['team_name'])


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
            print(team['team_page'] + "\t" + team['team_name'])

            # go to the right season's page
            for season_option in default_team_page('.team_season_switcher > option'):
                opt = pq(season_option)
                if opt.text() == "Pre-season - 2019 (history)" and season_id == "vrml_preseason":
                    team['team_page'] = baseURL + \
                        "/EchoArena/Teams/" + opt.attr('value')
                    break
                if opt.text() == "Season 1 - 2020 (history)" and season_id == "vrml_season_1":
                    team['team_page'] = baseURL + \
                        "/EchoArena/Teams/" + opt.attr('value')
                    break
                if opt.text() == "Season 2 - 2020" and season_id == "vrml_season_2":
                    team['team_page'] = baseURL + \
                        "/EchoArena/Teams/" + opt.attr('value')
                    break

            # actually go to the team page for the correct season and get more stats from there
            success = False
            while not success:
                try:
                    team_page = pq(team['team_page'])
                    success = True
                except:
                    print("Failed to load. Retrying...")
            

            roster = []
            if season_id == "vrml_season_2":
                past_roster = team_page('.players_container .player_name')
            else:
                past_roster = team_page(
                    '.teams_roster_season_container .player_name')

            for p in past_roster:
                roster.append(pq(p).text())
            team['roster'] = roster



            team['bio'] = team_page('.bio-text').html()
            rawpage = team_page.outer_html()
            discordIndex = rawpage.find('discord.gg/')
            if discordIndex > 0:
                discordEndIndex = rawpage.find('&quot;', discordIndex)
                if discordEndIndex < 0 or discordEndIndex - discordIndex > 50:
                    discordEndIndex = rawpage.find('"', discordIndex)
                team['discord'] = rawpage[discordIndex:discordEndIndex]


            # scrape the match history on the team page
            season_matches = []
            for matchHTML in team_page('.teams_recent_matches_table > tbody > tr'):
                match_pq = pq(matchHTML)
                match = {}
                match['match_id'] = match_pq(
                    '.match-page-info > a').attr('href').split('/')[3]
                match['match_time'] = match_pq('.date_recent_cell').text()
                match['teams'] = [
                    {
                        'team_name': match_pq('.home_team_cell').text(),
                        'score': match_pq('.score_cell').text().split(' ')[0],
                    },
                    {
                        'team_name': match_pq('.away_team_cell').text(),
                        'score': match_pq('.score_cell').text().split(' ')[2]
                    }
                ]
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

            if season_id not in matches:
                matches[season_id] = {}
            for sm in season_matches:
                matches[season_id][sm['match_id']] = sm

            # start adding this stuff to teams.json
            if team['team_name'] not in teams:
                teams[team['team_name']] = {}
            t = teams[team['team_name']]

            team_id = str(team['team_page'].split('/')[-1])

            # TODO remove
            # check if this team name was already used by a different team id
            if 'vrml_team_id' in t and t['vrml_team_id'] != team_id:
                # this is due to different seasons having different team ids
                print("Conflicting team names: " + team['team_name'])

            
            if season_id == "vrml_season_2" or 'vrml_team_id' not in t:
                t['vrml_team_id'] = team_id
                t['vrml_team_page'] = team['team_page']
            t['vrml_team_logo'] = team['team_logo']
            t['vrml_region'] = team['region']
            t['vrml_region_logo'] = team['region_logo']
            if 'discord' in team:
                t['discord'] = team['discord']
            t['bio'] = team['bio']

            if 'series' not in t:
                t['series'] = {}
            if season_id not in t['series']:
                t['series'][season_id] = {}
            teams_season = t['series'][season_id]
            if 'old_team_name' in team:
                teams_season['team_name'] = team['old_team_name']
            teams_season['vrml_team_id'] = team_id
            teams_season['vrml_team_page'] = team['team_page']
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

    with open('data/teams.json', 'w') as f:
        json.dump(teams, f, indent=4)

    with open('data/matches.json', 'w') as f:
        json.dump(matches, f, indent=4)


def scrapeVRMLPlayers():
    with open('data/players.json', 'r') as f:
        players = json.load(f)

    for season_id, season in seasons_data.items():
        if season['api_type'] != 'vrml':
            continue
        page = pq(season['players_url'])
        if season_id == 'vrml_season_2':
            numPlayers = int(page('.players-list-header-count').text()[20:23])
        else:
            numPlayers = int(page('.players-list-header-count').text()[0:4])

        for i in range(0, int(numPlayers/100)+1):
            page = pq(season['players_url']+"?posMin="+str(i*100+1))

            for playerHTML in page('.vrml_table_row'):
                player_pq = pq(playerHTML)
                pname = player_pq('.player_cell > a > span').text()

                if pname not in players:
                    players[pname] = {}
                player = players[pname]

                player['player_name'] = pname
                player['vrml_player_page'] = baseURL + \
                    player_pq('.player_cell > a').attr('href')
                player['vrml_player_logo'] = baseURL + \
                    player_pq('.player_cell > a > img').attr('src')
                player['vrml_team_name'] = player_pq(
                    '.team_cell > a > span').text()
                player['vrml_team_page'] = baseURL + \
                    player_pq('.team_cell > a').attr('href')
                player['vrml_team_logo'] = baseURL + \
                    player_pq('.team_cell > a > img').attr('src')
                nat_img_cell = player_pq('.nationality_cell > img')
                if nat_img_cell:
                    player['vrml_nationality'] = nat_img_cell.attr('title')
                    player['vrml_nationality_logo'] = baseURL + \
                        nat_img_cell.attr('src')
                else:
                    player['vrml_nationality'] = None
                    player['vrml_nationality_logo'] = None

    # Insert into DB
    # insertIntoDB(players, 'players', 'player_name')

    with open('data/players.json', 'w') as f:
        json.dump(players, f)


# only gets stats and rosters for the current season. This is faster than getting full stats
def scrapeCurrentSeasonTeamStats(season_name):
    with open('data/teams.json', 'r') as f:
        teams = json.load(f)

    with open('data/players.json', 'r') as f:
        players = json.load(f)

    # loop through the players and get their teams
    page = pq(seasons_data[season_name]['players_url'])
    print(seasons_data[season_name]['players_url'])

    if season_name == 'vrml_season_2':
        numPlayers = int(page('.players-list-header-count').text()[20:23])
    else:
        numPlayers = int(page('.players-list-header-count').text()[0:4])


    # load the team standing page
    another_page = True
    page_num = 0

    while another_page:
        page = pq(seasons_data[season_name]['standings_url']+"?rankMin="+str(page_num*100+1))
        print(seasons_data[season_name]['standings_url']+"?rankMin="+str(page_num*100+1))
        page_num += 1
        another_page = False
        for teamHTML in page('.standings_information > .vrml_table_container > .vrml_table > tbody > tr'):
            team_pq = pq(teamHTML)
            team_name = team_pq('.team_name').text()

            if team_name is None or team_name == '':
                if team_pq('.glyphicon-menu-down'):
                    another_page = True
                else:
                    print("skipping team. No team name.")
                continue

            if team_name not in teams:
                teams[team_name] = {}

            team = teams[team_name]

            if 'series' not in team:
                team['series'] = {}
            if season_name not in team['series']:
                team['series'][season_name] = {}
            season_team = team['series'][season_name]
            
            team['vrml_team_page'] = baseURL + team_pq('.team_link').attr('href')   # this may not be necessary here. There are also team pages for 
            season_team['vrml_team_page'] = baseURL + team_pq('.team_link').attr('href')
            team['vrml_team_logo'] = baseURL + team_pq('.team_logo').attr('src')
            season_team['division'] = team_pq('.div_cell > img').attr('title')
            season_team['division_logo'] = baseURL + \
                team_pq('.div_cell > img').attr('src')
            season_team['rank'] = team_pq('.pos_cell').text()
            team['region'] = team_pq('.group_cell > img').attr('title')
            team['region_logo'] = baseURL + \
                team_pq('.group_cell > img').attr('src')
            season_team['games_played'] = team_pq('.gp_cell').text()
            season_team['wins'] = team_pq('.win_cell').text()
            season_team['losses'] = team_pq('.loss_cell').text()
            season_team['points'] = team_pq('.pts_cell').text()
            season_team['mmr'] = team_pq('.mmr_cell').text()



    for i in range(0, int(numPlayers/100)+1):
        page = pq(seasons_data[season_name]
                  ['players_url']+"?posMin="+str(i*100+1))
        print(seasons_data[season_name]['players_url']+"?posMin="+str(i*100+1))

        for playerHTML in page('.vrml_table_row'):
            player_pq = pq(playerHTML)
            pname = player_pq('.player_cell > a > span').text()

            if pname not in players:
                players[pname] = {}
            player = players[pname]

            player['player_name'] = pname
            player['vrml_player_page'] = baseURL + \
                player_pq('.player_cell > a').attr('href')
            player['vrml_player_logo'] = baseURL + \
                player_pq('.player_cell > a > img').attr('src')
            player['vrml_team_name'] = player_pq(
                '.team_cell > a > span').text()
            player['vrml_team_page'] = baseURL + \
                player_pq('.team_cell > a').attr('href')
            player['vrml_team_logo'] = baseURL + \
                player_pq('.team_cell > a > img').attr('src')
            nat_img_cell = player_pq('.nationality_cell > img')
            if nat_img_cell:
                player['vrml_nationality'] = nat_img_cell.attr('title')
                player['vrml_nationality_logo'] = baseURL + \
                    nat_img_cell.attr('src')
            else:
                player['vrml_nationality'] = None
                player['vrml_nationality_logo'] = None


            # add this player to the team roster as well
            if player['vrml_team_name'] not in teams:
                print("Team doesn't exist in teams")
                return
            if 'series' not in teams[player['vrml_team_name']]:
                teams[player['vrml_team_name']]['series'] = {}
            if season_name not in teams[player['vrml_team_name']]['series']:
                teams[player['vrml_team_name']]['series'][season_name] = {}
            if 'roster' not in teams[player['vrml_team_name']]['series'][season_name]:
                teams[player['vrml_team_name']]['series'][season_name]['roster'] = []
            if player['player_name'] not in teams[player['vrml_team_name']]['series'][season_name]['roster']:
                teams[player['vrml_team_name']]['series'][season_name]['roster'].append(player['player_name'])


    with open('data/teams.json', 'w') as f:
        json.dump(teams, f, indent=4)

    with open('data/players.json', 'w') as f:
        json.dump(players, f, indent=4)


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


def scrapeESLMatchPages():

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
                                'esl_player_page': baseURLESL + player('a').attr('href'),
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
def add_players_matches():
    with open('data/players.json', 'r') as f:
        players = json.load(f)

    with open('data/teams.json', 'r') as f:
        teams = json.load(f)

    # there shouldn't be a previous matches.json
    if os.path.exists('data/matches.json'):
        with open('data/matches.json', 'r') as f:
            matches = json.load(f)
    else:
        matches = {}

    # loop through all the season files
    for file in seasons_data.items():
        if os.path.exists(file[1]['file']):
            with open(file[1]['file'], 'r') as f:
                esl_data = json.load(f)

            # # loop through all the teams in that season
            # for team in esl_data['teams'].items():
            #     team_name = team[0]

            #     # loop through the players on that team
            #     if 'roster' in team[1]:
            #         for player in team[1]['roster']:

            #             if player['name'] not in players:
            #                 players[player['name']] = {}
            #             p = players[player['name']]
            #             p['player_name'] = player['name']
            #             p['esl_player_page'] = player['player_page']
            #             p['esl_player_id'] = player['id']

            #             if 'teams' not in p:
            #                 p['teams'] = []

            #             if team_name not in p['teams']:
            #                 p['teams'].append(team_name)

            #     if team_name not in teams:
            #         teams[team_name] = {}

            #     t = teams[team_name]
            #     t['esl_team_id'] = team[0]

            # loop through all the cups in the season
            for cup in esl_data['cups']:
                # for each match in the cup
                for match in cup['matches']:
                    # this overwrites any old match data
                    matches[match['id']] = match

                    # loop through the 2 teams in this match
                    for team in match['teams']:
                        if team['team_name'] is None:
                            continue

                        # if the team doesn't exist, create it
                        if team['team_name'] not in teams:
                            teams[team['team_name']] = {
                                "esl_team_id": team['id'],
                                "esl_team_page": team['team_page'],
                                "esl_team_logo": team['team_logo']
                            }

                        # add the roster to the current season for each team
                        t = teams[team['team_name']]
                        if 'series' not in t:
                            t['series'] = {}
                        if file[0] not in t['series']:
                            t['series'][file[0]] = {}
                        if 'roster' not in t['series'][file[0]]:
                            t['series'][file[0]]['roster'] = {}
                        if 'matches' not in t['series'][file[0]] or isinstance(t['series'][file[0]]['matches'], dict):
                            t['series'][file[0]]['matches'] = []

                        # this overwrites any old match data
                        if match['id'] not in t['series'][file[0]]['matches']:
                            t['series'][file[0]]['matches'].append(match['id'])

                        if 'roster' in team:
                            # the roster for this match
                            new_roster = team['roster']
                            # the historical roster for this season
                            season_roster = t['series'][file[0]]['roster']
                            # loop through the players
                            for p in new_roster:
                                if p['player_name'] not in season_roster:
                                    season_roster[p['player_name']] = {
                                        'game_count': 1,
                                        'esl_player_id': p['esl_player_id'],
                                        'esl_player_logo': p['esl_player_logo'],
                                        'esl_player_page': p['esl_player_page']
                                    }
                                else:
                                    season_roster[p['player_name']
                                                  ]['game_count'] += 1

                                if p['player_name'] not in players:
                                    print("player doesn't exist. problem")
                                    return
                                playa = players[p['player_name']]

                                if 'series' not in playa:
                                    playa['series'] = {}
                                if file[0] not in playa['series']:
                                    playa['series'][file[0]] = {
                                        'teams': {},
                                        'matches': []
                                    }
                                # add the match to the match history for this player
                                if 'matches' in playa:
                                    del playa['matches']
                                if match['id'] not in playa['series'][file[0]]['matches']:
                                    playa['series'][file[0]]['matches'].append(
                                        match['id'])

                                # add the team to the team history for the player
                                if team['id'] not in playa['series'][file[0]]['teams']:
                                    playa['series'][file[0]]['teams'][team['id']] = {
                                        'game_count': 1
                                    }
                                else:
                                    playa['series'][file[0]
                                                    ]['teams'][team['id']]['game_count'] += 1

    with open('data/players.json', 'w') as f:
        json.dump(players, f, indent=4)

    with open('data/teams.json', 'w') as f:
        json.dump(teams, f, indent=4)

    with open('data/matches.json', 'w') as f:
        json.dump(matches, f, indent=4)


# adds vrml teams played for, matches casted, and matches cammed to players.json
def add_teams_to_players_vrml():
    with open('data/teams.json', 'r') as f:
        teams = json.load(f)

    with open('data/matches.json', 'r') as f:
        matches = json.load(f)

    with open('data/players.json', 'r') as f:
        players = json.load(f)

    # add teams played for to player
    for team_name, team in teams.items():
        if 'series' in team:
            for season_name, season in team['series'].items():
                if 'vrml' in season_name:
                    for player in season['roster']:
                        if player not in players:
                            print('player not found: problem: ' + caster)
                        else:
                            p = players[player]
                            if 'series' not in p:
                                p['series'] = {}
                            if season_name not in p['series']:
                                p['series'][season_name] = {}
                            if 'teams' not in p['series'][season_name]:
                                p['series'][season_name]['teams'] = []
                            if team_name not in p['series'][season_name]['teams']:
                                p['series'][season_name]['teams'].append(
                                    team_name)

    # add matches casted by player
    for season_name, season in seasons_data.items():
        if season_name in matches:
            for match_id, match in matches[season_name].items():
                if 'casters' in match:
                    for caster in match['casters']:
                        if caster not in players:
                            players[caster] = {}
                            players[caster]['player_name'] = caster
                        p = players[caster]
                        if 'series' not in p:
                            p['series'] = {}
                        if season_name not in p['series']:
                            p['series'][season_name] = {}
                        if 'matches_casted' not in p['series'][season_name]:
                            p['series'][season_name]['matches_casted'] = []
                        if match_id not in p['series'][season_name]['matches_casted']:
                            p['series'][season_name]['matches_casted'].append(
                                match_id)

    # add matches camera-manned by player
    for season_name, season in seasons_data.items():
        if season_name in matches:
            for match_id, match in matches[season_name].items():
                if 'cameramen' in match:
                    for cammer in match['cameramen']:
                        if cammer not in players:
                            players[cammer] = {}
                            players[cammer]['player_name'] = cammer
                        p = players[cammer]
                        if 'series' not in p:
                            p['series'] = {}
                        if season_name not in p['series']:
                            p['series'][season_name] = {}
                        if 'matches_cammed' not in p['series'][season_name]:
                            p['series'][season_name]['matches_cammed'] = []
                        if match_id not in p['series'][season_name]['matches_cammed']:
                            p['series'][season_name]['matches_cammed'].append(
                                match_id)

    with open('data/players.json', 'w') as f:
        json.dump(players, f, indent=4)


# def merge_aka_teams():
#     with open('data/teams.json', 'r') as f:
#         teams = json.load(f)

#     # add teams played for to player
#     for team_name, team in teams.items():
#         if 'aka' in team_name:

#         if 'series' in team:
#             for season_name, season in team['series'].items():
#                 if 'vrml' in season_name:

# scrapePlayers()
# scrapeMatches()
# scrapeTeams()
# downloadImages()
# uploadImages()

scrapeESLCups()
scrapeESLTeams()
scrapeESLMatchPages()

scrapeVRMLTeams()
scrapeVRMLPlayers()
add_players_matches()
add_teams_to_players_vrml()


# scrapeCurrentSeasonTeamStats("vrml_season_2")

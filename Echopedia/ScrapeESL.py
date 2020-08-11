import json
import os

from pyquery import PyQuery as pq

from WikiCommon import *
import LocalInternet

baseURLESL = 'https://play.eslgaming.com'

LocalInternet.load()

# Gets all VRCL/VRL matches from na/eu using API and returns the result as a dict
# resets data added to cup json files
def scrapeESLCups():
    teams = loadJSON('teams')

    for season_name, season in seasons_data.items():
        if season['api_type'] != 'esl':
            continue

        esl_data = loadJSON(season_name)
        
        season_teams = {}  # list of all teams in this season

        baseURL = "https://play.eslgaming.com"

        for url_region, url in season['api_urls'].items():
            print(url)
            result = LocalInternet.get(url)
            cups = json.loads(result)
            for cup_name, cup in cups.items():

                # skip s3 in s2
                if '2019-' in cup['uri'] and season_name == 'vrl_s2':
                    continue

                # skip s2 in s3
                if '2019-' not in cup['uri'] and season_name == 'vrl_s3':
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
                print(contestantsURL)
                result = LocalInternet.get(contestantsURL)
                contestants = json.loads(result)
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
                print(matchesURL)
                result = LocalInternet.get(matchesURL)
                matches = json.loads(result)
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

        dumpJSON(season_name, esl_data)
        
    dumpJSON('teams', teams)

    LocalInternet.save()


# Gets all teams and players on teams from ESL site
# gets teams from json file, exports to json file
def scrapeESLTeams():

    teams = loadJSON('teams')

    for team_name, team in teams.items():
        # skip teams that are not from ESL
        if 'esl_team_id' not in team:
            continue

        teamPageURL = "https://play.eslgaming.com/team/" + \
            str(team['esl_team_id'])
        teamPage = LocalInternet.local_pq(teamPageURL)
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

    dumpJSON('teams', teams)

    LocalInternet.save()


def scrapeESLMatchPages():

    players = loadJSON('players')

    for season_name, season in seasons_data.items():
        if season['api_type'] != 'esl':
            continue
        
        cups = loadJSON(season_name)

        # loop through all the cups in this season
        for cup in cups['cups']:
            # loop through all the matches in this cup
            for match in cup['matches']:
                # get the match page
                match['match_page'] = cup['link'] + 'match/' + str(match['id'])
                matchPage = LocalInternet.local_pq(match['match_page'])
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

        dumpJSON(season_name, cups)

    dumpJSON('players', players)

    LocalInternet.save()
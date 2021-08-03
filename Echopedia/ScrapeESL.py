import json
import os
import asyncio
import re

from datetime import datetime
from pyppeteer import launch
from pyquery import PyQuery as pq

from WikiCommon import *
import LocalInternet

baseURLESL = 'https://play.eslgaming.com'

LocalInternet.load()

# Gets all VRCL/VRL matches from na/eu using API and saves the result
# resets data added to cup json files
def scrapeESLCups():
    print("scrapeESLCups")

    teams = loadJSON('teams')
    matches = loadJSON('matches')

    for season_name, season in seasons_data.items():
        if season['api_type'] != 'esl':
            continue
        
        if season_name not in matches:
            matches[season_name] = {}
        esl_data = matches[season_name]
        
        season_teams = {}  # list of all teams in this season

        baseURL = "https://play.eslgaming.com"

        for url_region, url in season['api_urls'].items():
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
                result = LocalInternet.get(contestantsURL)
                contestants = json.loads(result)
                for c in contestants:
                    
                    if c['id'] not in cup_data['teams']:
                        cup_data['teams'][c['id']] = {}
                    cup_data['teams'][c['id']]['team_name'] = c['name']
                    cup_data['teams'][c['id']]['region'] = c['region']

                    if c['name'] not in teams:
                        teams[c['name']] = {}
                    teams[c['name']]['esl_team_id'] = c['id']

                    if c['name'] not in season_teams:
                        season_teams[c['name']] = {}
                    season_teams[c['name']]['esl_team_id'] = c['id']

                # get full count of teams
                cup_data['team_count'] = len(contestants)

                # get matches
                matchesURL = "https://api.eslgaming.com/play/v1/leagues/" + \
                    str(cup['id']) + "/matches"
                result = LocalInternet.get(matchesURL)
                local_matches = json.loads(result)
                for m in local_matches:
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

        
    dumpJSON('matches', matches)
    dumpJSON('teams', teams)

    LocalInternet.save()


# Gets all teams and players on teams from ESL site
# gets teams from json file, exports to json file
def scrapeESLTeams():
    print("scrapeESLTeams")

    teams = loadJSON('teams')

    for team_name, team in teams.items():
        # skip teams that are not from ESL
        if 'esl_team_id' not in team:
            continue

        teamPageURL = "https://play.eslgaming.com/team/" + \
            str(team['esl_team_id'])
        teamPage = LocalInternet.local_pq(teamPageURL)
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

        # PLAYERS ARE NOT USED FROM HERE, RATHER FROM INDIVIDUAL MATCHES
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
    print("scrapeESLMatchPages")

    players = loadJSON('players')
    teams = loadJSON('teams')
    matches = loadJSON('matches')

    for season_name, season in seasons_data.items():
        if season['api_type'] != 'esl':
            continue
        
        cups = matches[season_name]

        # loop through all the cups in this season
        for cup in cups['cups']:
            # loop through all the matches in this cup
            for match in cup['matches']:
                # get the match page
                match['match_page'] = cup['link'] + 'match/' + str(match['id'])
                matchPage = LocalInternet.local_pq(match['match_page'])

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
                        print("Different team name: " + new_team_name + " != " + team['team_name'])
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
                            p['esl_player_page'] = baseURLESL + "/echoarena/player/" + str(player_data['esl_player_id'])
                            p['esl_player_id'] = player_data['esl_player_id']
                            p['esl_player_logo'] = player_data['esl_player_logo']


                    
                    # add the match to teams.json for the team
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
                    if season_name not in t['series']:
                        t['series'][season_name] = {}
                    if 'roster' not in t['series'][season_name]:
                        t['series'][season_name]['roster'] = {}
                    if 'matches' not in t['series'][season_name] or isinstance(t['series'][season_name]['matches'], dict):
                        t['series'][season_name]['matches'] = []

                    # this overwrites any old match data
                    if match['id'] not in t['series'][season_name]['matches']:
                        t['series'][season_name]['matches'].append(match['id'])

                    if 'roster' in team:
                        # the roster for this match
                        new_roster = team['roster']
                        # the historical roster for this season
                        season_roster = t['series'][season_name]['roster']
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
                                season_roster[p['player_name']]['game_count'] += 1

                            if p['player_name'] not in players:
                                print("player doesn't exist. problem")
                                return
                            playa = players[p['player_name']]

                            if 'series' not in playa:
                                playa['series'] = {}
                            if season_name not in playa['series']:
                                playa['series'][season_name] = {
                                    'teams': {},
                                    'matches': []
                                }
                            # add the match to the match history for this player
                            if 'matches' in playa:
                                del playa['matches']
                            if match['id'] not in playa['series'][season_name]['matches']:
                                playa['series'][season_name]['matches'].append(
                                    match['id'])

                            # add the team to the team history for the player
                            if team['id'] not in playa['series'][season_name]['teams']:
                                playa['series'][season_name]['teams'][team['id']] = {
                                    'game_count': 1
                                }
                            else:
                                playa['series'][season_name]['teams'][team['id']]['game_count'] += 1


    dumpJSON('matches', matches)
    dumpJSON('players', players)
    dumpJSON('teams', teams)

    LocalInternet.save()




# loads each team history page and gets the full activity history 
# this doesn't work because of captcha
def scrapeESLTeamLogPages():
    print("scrapeESLTeamLogPages")

    teams = loadJSON('teams')

    for team_name, team_data in teams.items():
        if 'esl_team_page' not in team_data: continue

        tpage = team_data['esl_team_page']
        index = tpage.rindex('/')
        historyPageURL = tpage[:index] + '/log' + tpage[index:]
        historyPage = LocalInternet.local_pq(historyPageURL)

        print(historyPage.html())
        print(historyPage('.esl-content'))
        for row in historyPage('.esl-content table tr').items():
            print(row('td').text())

        break


async def scrapeESLTeamLogPagesPyppeteer():
    print("scrapeESLTeamLogPages")

    teams = loadJSON('teams')
    players = loadJSON('players')

    for team_name, team_data in teams.items():
        if 'esl_team_page' not in team_data:
            continue

        tpage = team_data['esl_team_page']
        index = tpage.rindex('/')
        historyPageURL = tpage[:index] + '/log' + tpage[index:]

        historyPageContent = await LocalInternet.innerHTMLPuppet(historyPageURL)

        roster_changes = []
        name_changes = []

        index = 0
        for row in historyPageContent('.esl-content table tr').items():
            index += 1
            if index < 3:
                continue
            print(row.children().text())
            if row.children().text() == '':
                continue
            timestamp_text = row('td:nth-child(1)').text()
            timestamp = datetime.strptime(timestamp_text, '%d.%m.%y %H:%Mh')
            event = row('td:nth-child(2) b').text()

            # roster change
            if event == 'register_team' or event == 'new_member' or event == 'kick_member':

                if event == 'kick_member':
                    userid = int(re.search('/(\d*)/', row('td:nth-child(2) a').attr('href')).group(1))
                    kicked_by = re.search('by (.*) \(\d*\)', row('td:nth-child(2) a').text()).group(1)
                    kicked_by_id = re.search('by .* \((\d*)\)', row('td:nth-child(2) a').text()).group(1)
                    username = next((pname for pname, p in players.items() if 'esl_player_id' in p and p['esl_player_id'] == userid), None)
                    if username is None:
                        print("Can't find player in list of players")
                        continue

                    roster_changes.append({
                        'timestamp': timestamp.isoformat(),
                        'action': event,
                        'player_name': username,
                        'player_id': userid,
                        'kicked_by_name': kicked_by,
                        'kicked_by_id': kicked_by_id,
                    })
                    player_roster_change_dict = {
                        'timestamp': timestamp.isoformat(),
                        'action': event,
                        'team_name': team_name,
                        'kicked_by_name': kicked_by,
                        'kicked_by_id': kicked_by_id,
                    }
                else:
                    user = row('td:nth-child(2) a').text()
                    username_match = re.search('(.*) \(\d*\)', user)
                    username = username_match.group(1)
                    userid = int(re.search(' \((\d*)\)', user).group(1))
                    roster_changes.append({
                        'timestamp': timestamp.isoformat(),
                        'action': event,
                        'player_name': username,
                        'player_id': userid
                    })
                    player_roster_change_dict = {
                        'timestamp': timestamp.isoformat(),
                        'action': event,
                        'team_name': team_name,
                    }

                if username not in players:
                    print("couldn't find player name in players.json: " + username)
                    continue

                # if this is the first entry
                if 'esl_roster_changes' not in players[username]:
                    players[username]['esl_roster_changes'] = []
                # if any duplicate entry, delete the whole thing
                if any(r['timestamp'] == timestamp.isoformat() for r in players[username]['esl_roster_changes']):
                    players[username]['esl_roster_changes'] = []
                players[username]['esl_roster_changes'].append(player_roster_change_dict)
                
            # name change
            elif event == 'change_name':
                line_end = row('td:nth-child(2)').remove('b').text()
                name_changes.append({
                    'timestamp': timestamp.isoformat(),
                    'new_name': line_end
                })
            

        if team_name not in teams:
            print("couldn't find team name in teams.json: " + team_name)
            continue

        teams[team_name]['esl_roster_changes'] = roster_changes
        teams[team_name]['esl_name_changes'] = name_changes

    dumpJSON('players', players)
    dumpJSON('teams', teams)

asyncio.get_event_loop().run_until_complete(scrapeESLTeamLogPagesPyppeteer())

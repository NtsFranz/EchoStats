import requests
from pyquery import PyQuery as pq
from pathlib import Path
import os
import datetime
import json

from WikiCommon import *
import ScrapeESL
import ScrapeVRML


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

ScrapeESL.scrapeESLCups()
ScrapeESL.scrapeESLTeams()
ScrapeESL.scrapeESLMatchPages()

ScrapeVRML.scrapeVRMLTeams()
ScrapeVRML.scrapeVRMLPlayers()
# add_players_matches()
# add_teams_to_players_vrml()


# ScrapeVRML.scrapeCurrentSeasonTeamStats("vrml_season_2")

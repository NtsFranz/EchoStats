import requests
import json
from string import Template
from datetime import datetime

from WikiBotSetup import *
from WikiCommon import *


table_header = '{| class="wikitable sortable"\n'
table_header_nonsortable = '{| class="wikitable"\n'
table_row = '|-\n'
table_footer = '|}\n'


def UploadSeasonCupsESL():
    # load the data into an object from file
    with open('data/VRCL_S1_cups.json') as f:
        esl_data = json.load(f)

    esl_data['cups'] = sorted(esl_data['cups'], key=lambda i: i['date'])

    # Create the table string
    table_str = table_header
    table_str += table_row
    table_str += '! Date !! Cup Name !! External Cup Page !! Number of Teams\n'

    # add rows to the table string
    for cup in esl_data['cups']:
        table_str += table_row
        row = Template(
            '| $date || [[$match_page|$name]] || [$link ESL Cup Page] || $num_teams\n')
        # date = datetime.strptime(cup['date'], '%Y-%m-%dT%H:%M:s'
        date = datetime.fromisoformat(cup['date']).strftime(
            '%Y-%m-%d %H:%M') if cup['date'] != 'n/a' else 'n/a'
        row = row.substitute({
            "date": date,
            # "date": cup['date'],
            "name": cup['name'],
            "match_page": cup['name'].replace(' ', '_').replace('#', ''),
            "link": cup['link'],
            "num_teams": len(cup['teams'])
        })
        table_str += row
    table_str += table_footer

    # write the table result to an outfile
    with open('data/out.txt', 'w') as out:
        out.write(table_str)


def GenerateSeasonPagesVRML():
    # load the data into an object from file
    with open('data/matches.json') as f:
        matches = json.load(f)

    for season_name, season in seasons_data.items():
        if season_name in matches:

            page = ""

            page += "=== Matches ===\n"

            page += table_header
            page += table_row
            page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team !! Video URL\n'

            matches_list = sorted(matches[season_name].items(), key=lambda i: i[1]['match_time'])
            for matchobj in matches_list:
                match = matchobj[1]
                page += table_row
                row = Template(
                    '| $time || [$match_page VRML Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]] || [$video_url Video Link]\n')
                page += row.substitute({
                    "time": match["match_time"],
                    "match_page": match['match_page'],
                    "home_team_name": match['teams'][0]['team_name'],
                    "home_team_score": match['teams'][0]['score'],
                    "away_team_score": match['teams'][1]['score'],
                    "away_team_name": match['teams'][1]['team_name'],
                    "video_url": match['video_url']
                })

            page = page.replace("[None Video Link]", "No Video")
            page += table_footer

            createPage(season['wiki_page'], page)


# Creates pages with a list of matches for each cup
def UploadCupMatchPagesESL():
    for season in seasons_data.items():
        # load the data into an object from file
        with open(season[1]['file']) as f:
            esl_data = json.load(f)

        for cup in esl_data['cups']:
            page = "This cup is a part of the VR Challenger League. See the [[" + \
                season[1]['wiki_page']+"|full list of cups]].\n\n"

            page += "[" + cup['link'] + " ESL Cup Page]\n\n"

            if "registration" in cup['link']:
                page += "This cup is a registration cup, so it contains no matches.\n"
            else:
                page += "=== List of Matches ===\n"

                # Create the table string
                page += table_header
                page += table_row
                page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team\n'
                cup['matches'] = sorted(
                    cup['matches'], key=lambda i: i['match_time'])
                for m in cup['matches']:
                    page += table_row
                    row = Template(
                        '| $match_time || [$esl_match_page ESL Match Page] ||[[$home_team_name]] || $home_score || $away_score || [[$away_team_name]]\n')
                    date = datetime.fromisoformat(m['match_time']).strftime(
                        '%Y-%m-%d %H:%M') if m['match_time'] != 'n/a' else 'n/a'
                    row = row.substitute({
                        "match_time": date,
                        "esl_match_page": cup['link'] + '/match/' + str(m['id']),
                        "home_team_name": m['teams'][1]['team_name'],
                        "away_team_name": m['teams'][0]['team_name'],
                        "home_score": m['teams'][1]['score'],
                        "away_score": m['teams'][0]['score']
                    })
                    page += row
                page += table_footer

            page += "=== List of Teams ===\n"
            page += "Number of teams in this cup: " + \
                str(len(cup['teams'])) + "\n"

            # Create the table string
            page += table_header
            page += table_row
            page += '! Team Logo !! Team Name !! External Team Page\n'
            for t in cup['teams']:
                page += table_row
                row = Template(
                    '| $team_logo || [[$team_name]] || [$esl_team_page ESL Team Page]\n')
                row = row.substitute({
                    "team_logo": "",
                    "team_name": t['team_name'],
                    "esl_team_page": cup['link'] + '/team/' + str(t['id'])
                })
                page += row
            page += table_footer

            createPage(cup['name'].replace('#', ''), page)


def UploadTeamPages():
    # load the data into an object from file
    with open('data/teams.json') as f:
        teams = json.load(f)

    with open('data/matches.json') as f:
        matches = json.load(f)

    with open('data/players.json') as f:
        players = json.load(f)

    for teamItem in teams.items():
        if teamItem[0] == "Deleted account":
            continue
        team = teamItem[1]

        page = ""
        page += "[[Category:Team]]\n"
        page += "== Profile ==\n"

        # add VRML profile data
        if 'vrml_team_id' in team:
            page += "=== VRML ===\n"
            page += team['vrml_team_logo'] + '\n\n'
            page += "[" + team['vrml_team_page'] + " VRML Team Page]\n\n"
            page += "Region: " + team['vrml_region']
            page += " " + team['vrml_region_logo'] + "\n\n"

            # add season summary stats
            for series in team['series'].items():
                if 'vrml' in series[0]:
                    page += "==== " + \
                        seasons_data[series[0]]['name'] + " ====\n"
                    page += table_header_nonsortable
                    page += '! Division !! Rank !! Games Played !! Wins !! Losses !! Points !! MMR\n'
                    page += table_row
                    row = Template(
                        '| $division || $rank || $games_played || $wins || $losses || $points || $mmr\n')
                    page += row.substitute(series[1])
                    page += table_footer

        # add ESL profile data
        if "esl_team_id" in team:
            page += "=== ESL ===\n"
            if 'esl_team_logo' in team:
                page += team['esl_team_logo'] + "\n\n"
            page += "[" + team['esl_team_page'] + " ESL Team Page]\n\n"
            if "esl_founded" in team:
                page += "Founded: " + team['esl_founded'] + "\n\n"
            if "esl_region" in team:
                page += "Region: " + team['esl_region'] + "\n\n"

        if 'series' in team:
            # add roster info
            page += "== Roster ==\n"
            for series in team['series'].items():
                page += '=== ' + seasons_data[series[0]]['name'] + ' ===\n'
                page += table_header

                # VRML pages
                if 'vrml' in series[0]:
                    page += '! Player Logo !! Player Name\n'
                    for p in series[1]['roster']:
                        page += table_row
                        row = Template('| $player_logo || [[$player_name]]\n')
                        # row = Template('| [[$player_name]]\n')
                        page += row.substitute({
                            "player_name": p,
                            "player_logo": players[p]['vrml_player_logo']
                        })
                # ESL pages
                else:
                    page += '! Player Logo !! Player Name !! Games Played\n'
                    for p in series[1]['roster'].items():
                        page += table_row
                        row = Template(
                            '| $player_logo || [[$player_name]] || $game_count\n')
                        # row = Template('| [[$player_name]]\n')
                        page += row.substitute({
                            "player_name": p[0],
                            "game_count": p[1]['game_count'],
                            "player_logo": p[1]['esl_player_logo']
                        })

                page += table_footer

            page += "== Match History ==\n"
            for series in team['series'].items():
                if 'matches' in series[1]:
                    page += '=== ' + seasons_data[series[0]]['name'] + ' ===\n'
                    page += table_header

                    # VRML pages
                    if 'vrml' in series[0]:
                        page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team !! Video URL\n'
                        for match in series[1]['matches']:
                            page += table_row
                            row = Template(
                                '| $match_time || [$match_page VRML Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]] || [$video_url Video Link]\n')
                            page += row.substitute({
                                "match_time": match["match_time"],
                                "match_page": match['match_page'],
                                "home_team_name": match['teams'][0]['team_name'],
                                "home_team_score": match['teams'][0]['score'],
                                "away_team_score": match['teams'][1]['score'],
                                "away_team_name": match['teams'][1]['team_name'],
                                "video_url": match['video_url']
                            })

                    # ESL pages
                    else:
                        page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team\n'
                        for match in series[1]['matches']:
                            page += table_row
                            row = Template(
                                '| $match_time || [$match_page ESL Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]]\n')
                            m = matches[str(match)]
                            page += row.substitute({
                                "match_time": m["match_time"],
                                "match_page": m['match_page'],
                                "home_team_name": m['teams'][0]['team_name'],
                                "home_team_score": m['teams'][0]['score'],
                                "away_team_score": m['teams'][1]['score'],
                                "away_team_name": m['teams'][1]['team_name']
                            })

                    page += table_footer

        createPage(teamItem[0], page)


def UploadPlayerPages():
    with open('data/players.json', 'r') as f:
        players = json.load(f)

    with open('data/matches.json') as f:
        matches = json.load(f)

    with open('data/teams.json') as f:
        teams = json.load(f)

    for playerItem in players.items():
        if playerItem[0] == "Deleted account":
            continue
        player = playerItem[1]

        page = ""
        page += "[[Category:Player]]\n"
        page += "== Profile ==\n"

        # add VRML profile data
        if 'vrml_player_page' in player:
            page += "=== VRML ===\n"
            page += player['vrml_player_logo'] + '\n\n'
            page += "[" + player['vrml_player_page'] + " VRML Player Page]\n\n"
            if player['vrml_nationality'] is not None:
                page += "Region: " + player['vrml_nationality'] + "\n\n"
                # page += " " + player['vrml_nationality_logo'] + "\n\n"

        # add ESL profile data
        if "esl_player_id" in player:
            page += "=== ESL ===\n"
            if 'esl_player_logo' in player:
                page += player['esl_player_logo'] + "\n\n"
            player['esl_player_page'] = player['esl_player_page'].replace(
                "https://vrmasterleague.com", "https://play.eslgaming.com")
            page += "[" + player['esl_player_page'] + " ESL Player Page]\n\n"
            if "esl_founded" in player:
                page += "Founded: " + player['esl_founded'] + "\n\n"
            if "esl_region" in player:
                page += "Region: " + player['esl_region'] + "\n\n"

        if 'series' in player:
            # add roster info
            page += "== Teams ==\n"
            for season_name, season in seasons_data.items():
                if season_name not in player['series']:
                    continue

                if 'teams' in player['series'][season_name]:
                    page += '=== ' + season['name'] + ' ===\n'
                    page += table_header
                    if isinstance(player['series'][season_name]['teams'], list):
                        page += '! Team Logo !! Team Name\n'
                        for teamname in player['series'][season_name]['teams']:
                            if teamname is None or teamname not in teams:
                                continue
                            teamdata = teams[teamname]

                            page += table_row

                            # VRML pages
                            if 'vrml' not in season_name:
                                print("this should be a vrml series. problem")
                                return

                            row = Template('| $team_logo || [[$team_name]]\n')
                            # row = Template('| [[$team_name]]\n')
                            page += row.substitute({
                                "team_name": teamname,
                                "team_logo": teamdata['vrml_team_logo']
                            })
                        page += table_footer
                    else:
                        page += '! Team Logo !! Team Name !! Games Played\n'
                        for t in player['series'][season_name]['teams'].items():
                            teamname, teamdata = getTeamById(teams, t[0])
                            if teamname is None:
                                continue

                            page += table_row

                            # ESL pages
                            row = Template(
                                '| $team_logo || [[$team_name]] || $game_count\n')
                            # row = Template('| [[$team_name]]\n')
                            if 'esl_team_logo' in teamdata:
                                page += row.substitute({
                                    "team_name": teamname,
                                    "game_count": t[1]['game_count'],
                                    "team_logo": teamdata['esl_team_logo']
                                })
                            else:
                                page += row.substitute({
                                    "team_name": teamname,
                                    "game_count": t[1]['game_count'],
                                    "team_logo": "no logo"
                                })
                        page += table_footer

            page += "== Match History ==\n"
            for series in player['series'].items():
                if 'matches' in series[1] or 'matches_casted' in series[1] or 'matches_cammed' in series[1]:
                    page += '=== ' + seasons_data[series[0]]['name'] + ' ===\n'

                    # VRML pages
                    if 'vrml' in series[0]:
                        # add matches played (shouldn't exist yet)
                        if 'matches' in series[1]:
                            page += "==== Matches Played ====\n"
                            page += table_header
                            page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team !! Video URL\n'
                            for match in series[1]['matches']:
                                page += table_row
                                row = Template(
                                    '| $time || [$match_page VRML Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]] || [$video_url Video Link]\n')
                                m = matches[series[0]][match]
                                page += row.substitute({
                                    "time": m["match_time"],
                                    "match_page": m['match_page'],
                                    "home_team_name": m['teams'][0]['team_name'],
                                    "home_team_score": m['teams'][0]['score'],
                                    "away_team_score": m['teams'][1]['score'],
                                    "away_team_name": m['teams'][1]['team_name']
                                })
                            page += table_footer

                        # add matches casted
                        if 'matches_casted' in series[1]:
                            page += "==== Matches Casted ====\n"
                            page += table_header
                            page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team !! Video URL\n'
                            for match in series[1]['matches_casted']:
                                page += table_row
                                row = Template(
                                    '| $time || [$match_page VRML Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]] || [$video_url Video Link]\n')
                                m = matches[series[0]][match]
                                page += row.substitute({
                                    "time": m["match_time"],
                                    "match_page": m['match_page'],
                                    "home_team_name": m['teams'][0]['team_name'],
                                    "home_team_score": m['teams'][0]['score'],
                                    "away_team_score": m['teams'][1]['score'],
                                    "away_team_name": m['teams'][1]['team_name'],
                                    "video_url": m['video_url']
                                })
                            page += table_footer

                        # add matches cammed
                        if 'matches_cammed' in series[1]:
                            page += "==== Matches as Cameraman ====\n"
                            page += table_header
                            page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team !! Video URL\n'
                            for match in series[1]['matches_cammed']:
                                page += table_row
                                row = Template(
                                    '| $time || [$match_page VRML Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]] || [$video_url Video Link]\n')
                                m = matches[series[0]][match]
                                page += row.substitute({
                                    "time": m["match_time"],
                                    "match_page": m['match_page'],
                                    "home_team_name": m['teams'][0]['team_name'],
                                    "home_team_score": m['teams'][0]['score'],
                                    "away_team_score": m['teams'][1]['score'],
                                    "away_team_name": m['teams'][1]['team_name'],
                                    "video_url": m['video_url']
                                })
                            page += table_footer

                    # ESL pages
                    else:
                        if 'matches' in series[1]:
                            page += table_header
                            page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team\n'
                            for match in series[1]['matches']:
                                page += table_row
                                row = Template(
                                    '| $time || [$match_page ESL Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]]\n')
                                m = matches[str(match)]
                                page += row.substitute({
                                    "time": m["match_time"],
                                    "match_page": m['match_page'],
                                    "home_team_name": m['teams'][0]['team_name'],
                                    "home_team_score": m['teams'][0]['score'],
                                    "away_team_score": m['teams'][1]['score'],
                                    "away_team_name": m['teams'][1]['team_name']
                                })
                            page += table_footer

        createPage(playerItem[0], page)


def getTeamById(teams_dict, idstr):
    # ESL
    if len(idstr) == 8 or len(idstr) == 7:
        id = int(idstr)
        for name, data in teams_dict.items():
            if 'esl_team_id' in data and (data['esl_team_id'] == id or data['esl_team_id'] == idstr):
                return name, data

        return [None, None]
    # VMRL
    else:
        for name, data in teams_dict.items():
            if 'vrml_team_id' in data and data['vrml_team_id'] == idstr:
                return name, data

        return [None, None]


def createPage(pageName, pageData):
    # Step 4: POST request to edit a page
    PARAMS_3 = {
        "action": "edit",
        "title": pageName,
        "token": CSRF_TOKEN,
        "format": "json",
        "text": pageData
    }

    R = S.post(URL, data=PARAMS_3, headers=headers)
    DATA = R.json()

    print(DATA)


# UploadSeasonCupsESL()
# UploadCupMatchPagesESL()
# UploadTeamPages()
# UploadPlayerPages()
GenerateSeasonPagesVRML()

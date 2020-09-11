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


# verified 8/31/20
# updates the 3 cup pages
def UploadSeasonCupsESL():

    matches = loadJSON('matches')
    
    # loop through all the season files
    for season_name, season in seasons_data.items():

        if season['api_type'] != 'esl':
            continue

        # load the data into an object from file
        esl_data = matches[season_name]

        esl_data['cups'] = sorted(esl_data['cups'], key=lambda i: i['date'])
        
        # Create the table string
        table_str = {
            "na": table_header,
            "eu": table_header
        }
        table_str['na'] += table_row
        table_str['eu'] += table_row
        table_str['na'] += '! Date !! Cup Name !! External Cup Page !! Number of Teams\n'
        table_str['eu'] += '! Date !! Cup Name !! External Cup Page !! Number of Teams\n'

        # add rows to the table string
        for cup in esl_data['cups']:
            if 'north-america' in cup['link']:
                region = 'na'
            elif 'europe' in cup['link']:
                region = 'eu'
            else:
                print("EREREEREOR")
            table_str[region] += table_row
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
                "num_teams": cup['team_count']
            })
            table_str[region] += row
        table_str['na'] += table_footer
        table_str['eu'] += table_footer


        page = "[[Category:Series]]\n"
        page += "=== North America ===\n"
        page += table_str['na']
        page += "\n=== Europe ===\n"
        page += table_str['eu']

        # # write the table result to an outfile
        # path = os.path.join(os.path.dirname(__file__), 'data/'+season_name+'_cups_page.txt')
        # with open(path, 'w') as f:
        #     f.write(page)

        # upload to the wiki
        updatePage(season['wiki_page'], page)

# verified 8/31/20
# updates the 3 season pages
def GenerateSeasonPagesVRML():
    # load the data into an object from file
    matches = loadJSON('matches')

    for season_name, season in seasons_data.items():
        if seasons_data[season_name]['api_type'] == "vrml":

            page = ""
            page = "[[Category:Series]]\n"
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
                    "home_team_name": EscapePageLink(OnlyAKA(match['teams'][0]['team_name'])),
                    "home_team_score": match['teams'][0]['score'],
                    "away_team_score": match['teams'][1]['score'],
                    "away_team_name": EscapePageLink(OnlyAKA(match['teams'][1]['team_name'])),
                    "video_url": match['video_url']
                })

            page = page.replace("[None Video Link]", "No Video")
            page += table_footer

            updatePage(season['wiki_page'], page)


# verified 8/31/20
# Creates pages with a list of matches for each cup
def UploadCupMatchPagesESL():

    matches = loadJSON('matches')

    for season_name, season in seasons_data.items():
        if season['api_type'] != 'esl':
            continue

        # load the data into an object from file
        esl_data = matches[season_name]

        for cup in esl_data['cups']:
            page = "This cup is a part of the VR Challenger League. See the [[" + \
                season['wiki_page']+"|full list of cups]] for this season.\n\n"

            page += "[" + cup['link'] + " ESL Cup Page]\n\n"

            if "registration" in cup['link']:
                page += "This cup is a registration cup, so it contains no matches.\n"
            else:
                page += "=== List of Matches ===\n"

                # Create the table string
                page += table_header
                page += table_row
                page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team\n'
                cup['matches'] = sorted(cup['matches'], key=lambda i: i['match_time'])
                for m in cup['matches']:
                    page += table_row
                    row = Template('| $match_time || [$esl_match_page ESL Match Page] ||[[$home_team_name]] || $home_score || $away_score || [[$away_team_name]]\n')
                    date = datetime.fromisoformat(m['match_time']).strftime('%Y-%m-%d %H:%M') if m['match_time'] != 'n/a' else 'n/a'
                    row = row.substitute({
                        "match_time": date,
                        "esl_match_page": cup['link'] + '/match/' + str(m['id']),
                        "home_team_name": m['teams'][1]['team_name'],
                        "away_team_name": m['teams'][0]['team_name'],
                        "home_score": m['teams'][1]['score'],
                        "away_score": m['teams'][0]['score']
                    })
                    row = row.replace("[[None]]", "Deleted Team")
                    page += row
                page += table_footer

            page += "=== List of Teams ===\n"
            page += "Number of teams in this cup: " + \
                str(cup['team_count']) + "\n"

            # Create the table string
            page += table_header
            page += table_row
            page += '! Team Logo !! Team Name !! External Team Page\n'
            for team_id, team in cup['teams'].items():
                page += table_row
                row = Template('| $team_logo || [[$team_name]] || [$esl_team_page ESL Team Page]\n')
                row = row.substitute({
                    "team_logo": "",
                    "team_name": team['team_name'],
                    "esl_team_page": cup['link'] + 'team/' + str(team_id)
                })
                page += row
            page += table_footer

            updatePage(cup['name'].replace('#', ''), page)

# verified 9/6/20
def UploadTeamPages():

    # load the data into an object from file
    teams = loadJSON('teams')
    matches = loadJSON('matches')
    players = loadJSON('players')

    for team_name, team in teams.items():
        if team_name == "Deleted account":
            continue

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
            for series_name, series in team['series'].items():
                if 'vrml' in series_name:
                    page += "==== " + \
                        seasons_data[series_name]['name'] + " ====\n"
                    page += table_header_nonsortable
                    page += '! Division !! Rank !! Games Played !! Wins !! Losses !! Points !! MMR\n'
                    page += table_row
                    row = Template(
                        '| $division || $rank || $games_played || $wins || $losses || $points || $mmr\n')
                    page += row.substitute(series)
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
            for series_name, series in team['series'].items():
                if 'roster' in series and len(series['roster']) > 0:
                    page += '=== ' + seasons_data[series_name]['name'] + ' ===\n'
                    page += table_header

                    # VRML pages
                    if 'vrml' in series_name:
                        page += '! Player Logo !! Player Name\n'
                        for p in series['roster']:
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
                        for player_name, player_data in series['roster'].items():
                            page += table_row
                            row = Template(
                                '| $player_logo || [[$player_name]] || $game_count\n')
                            # row = Template('| [[$player_name]]\n')
                            page += row.substitute({
                                "player_name": player_name,
                                "game_count": player_data['game_count'],
                                "player_logo": player_data['esl_player_logo']
                            })

                    page += table_footer

            page += "== Match History ==\n"
            for series_name, series in team['series'].items():
                if 'matches' in series:
                    page += '=== ' + seasons_data[series_name]['name'] + ' ===\n'
                    page += table_header

                    # VRML pages
                    if seasons_data[series_name]["api_type"] == 'vrml':
                        page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team !! Video URL\n'
                        for match in series['matches']:
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
                    elif seasons_data[series_name]["api_type"] == 'esl':
                        page += '! Time !! External Match Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team\n'
                        for match in series['matches']:
                            page += table_row
                            row = Template(
                                '| $match_time || [$match_page ESL Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]]\n')
                            m = matches[series_name]['matches'][str(match)]
                            page += row.substitute({
                                "match_time": m["match_time"],
                                "match_page": m['match_page'],
                                "home_team_name": m['teams'][0]['team_name'],
                                "home_team_score": m['teams'][0]['score'],
                                "away_team_score": m['teams'][1]['score'],
                                "away_team_name": m['teams'][1]['team_name']
                            })

                    page += table_footer

        
        page = page.replace("[None Video Link]", "No Video")

        updatePage(team_name, page)

# verified 9/6/20
def UploadPlayerPages():


    # load the data into an object from file
    teams = loadJSON('teams')
    matches = loadJSON('matches')
    players = loadJSON('players')
    
    for player_name, player in players.items():
        if player_name == "Deleted account":
            continue

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
                                m = matches[series[0]]['matches'][str(match)]
                                page += row.substitute({
                                    "time": m["match_time"],
                                    "match_page": m['match_page'],
                                    "home_team_name": m['teams'][0]['team_name'],
                                    "home_team_score": m['teams'][0]['score'],
                                    "away_team_score": m['teams'][1]['score'],
                                    "away_team_name": m['teams'][1]['team_name']
                                })
                            page += table_footer

        updatePage(player_name, page)


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


def EscapePageLink(string: str) -> str:
    string = string.replace('[', '')
    string = string.replace(']', '')
    return string

def OnlyAKA(string: str) -> str:
    return string.split(' (aka ')[0]


def getPage(pageName):
        # Get the previous page
    params = {
        "action": "parse",
        "prop": "wikitext",
        "page": pageName,
        "format": "json",
        "formatversion": 2
    }

    r = S.get(URL, params=params, headers=headers)
    if r.status_code != 200:
        return None
    jsondata = json.loads(r.text)
    if 'error' in jsondata:
        return None
    data = jsondata['parse']['wikitext']
    return data


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

def updatePage(pageName, pageData):
    old_page = getPage(pageName)
    if old_page is None:
        createPage(pageName, pageData)
        return

    splitter = '<!-- CONTENT IS AUTOMATED BELOW THIS LINE. MAKE CHANGES ABOVE ONLY. -->'

    parts = old_page.split(splitter)

    if len(parts) == 1:
        parts = ['', old_page]
    elif len(parts) != 2:
        print("ERROR reading old page")
        return

    if not ezCompare(parts[1], pageData):
        new_data = parts[0] + splitter + "\n\n" + pageData
        createPage(pageName, new_data)
    else:
        print("Unchanged: " + pageName)

    
# compare without whitespaces
def ezCompare(str1, str2):
    str1 = str1.replace(' ', '')
    str1 = str1.replace('\\n', '')
    str1 = str1.replace('\n', '')

    str2 = str2.replace(' ', '')
    str2 = str2.replace('\\n', '')
    str2 = str2.replace('\n', '')

    return str1 == str2


UploadSeasonCupsESL()
UploadCupMatchPagesESL()

GenerateSeasonPagesVRML()

UploadTeamPages()
UploadPlayerPages()

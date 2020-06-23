import requests
import json
from string import Template
from datetime import datetime


from WikiBotSetup import *


table_header = '{| class="wikitable sortable"\n'
table_header_nonsortable = '{| class="wikitable"\n'
table_row = '|-\n'
table_footer = '|}\n'

season_names = {
    'vrcl_s1': 'VR Challenger League Season 1',
    'vrl_s2': 'VR League Season 2',
    'vrl_s3': 'VR League Season 3',
    'vrml_preseason': 'VR Master League Pre-season',
    'vrml_season_1': 'VR Master League Season 1',
    'vrml_season_2': 'VR Master League Season 2',
}

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
        row = Template('| $date || [[$match_page|$name]] || [$link ESL Cup Page] || $num_teams\n')
        #date = datetime.strptime(cup['date'], '%Y-%m-%dT%H:%M:s'
        date = datetime.fromisoformat(cup['date']).strftime('%Y-%m-%d %H:%M') if cup['date'] != 'n/a' else 'n/a'
        row = row.substitute({
            "date": date,
            #"date": cup['date'],
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

# Creates pages with a list of matches for each cup
def UploadCupMatchPagesESL():
    # load the data into an object from file
    with open('data/VRCL_S1_cups.json') as f:
        esl_data = json.load(f)

    for cup in esl_data['cups']:
        page = "This cup is a part of the VR Challenger League. See the [[VR Challenger League (ESL) List of Cups|full list of cups]].\n\n"

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
                page += row
            page += table_footer

        page += "=== List of Teams ===\n"
        page += "Number of teams in this cup: " + str(len(cup['teams'])) + "\n"

        # Create the table string
        page += table_header
        page += table_row
        page += '! Team Logo !! Team Name !! External Team Page\n'
        for t in cup['teams']:
            page += table_row
            row = Template('| $team_logo || [[$team_name]] || [$esl_team_page ESL Team Page]\n')
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

    for teamItem in teams.items():
        team = teamItem[1]

        page = ""

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
                    page += "==== " + season_names[series[0]] + " ====\n"
                    page += table_header_nonsortable
                    page += '! Division !! Rank !! Games Played !! Wins !! Losses !! Points !! MMR\n'
                    page += table_row
                    row = Template('| $division || $rank || $games_played || $wins || $losses || $points || $mmr\n')
                    page += row.substitute(series[1])
                    page += table_footer

        # add ESL profile data
        if "esl_team_id" in team:
            page += "=== ESL ===\n"
            page += team['esl_team_logo'] + "\n\n"
            page += "[" + team['esl_team_page'] + " ESL Team Page]\n\n"
            if "esl_founded" in team:
                page += "Founded: " + team['esl_founded'] + "\n\n"
            if "esl_region" in team:
                page += "Region: " + team['esl_region'] + "\n\n"

        # add roster info
        page += "== Roster ==\n"
        for series in team['series'].items():
            page += '=== ' + season_names[series[0]] + ' ===\n'
            page += table_header
            # page += '! Player Logo !! Player Name !! External Player Page\n'
            page += '! Player Name\n'
            for p in series[1]['roster']:
                page += table_row
                # row = Template('| $player_logo || [[$player_name]] || [$player_page ESL Player Page]\n')
                row = Template('| [[$player_name]]\n')
                page += row.substitute({
                    "player_name": p
                })
            page += table_footer

        page += "== Match History ==\n"
        for series in team['series'].items():
            if 'matches' in series[1]:
                page += '=== ' + season_names[series[0]] + ' ===\n'
                page += table_header
                page += '! Time !! External Cup Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team !! Video URL\n'
                for match in series[1]['matches']:
                    page += table_row
                    row = Template('| $time || [$match_page VRML Match Page] || [[$home_team_name]] || $home_team_score || $away_team_score || [[$away_team_name]] || [$video_url Video Link]\n')
                    page += row.substitute(match)
                page += table_footer

        createPage(teamItem[0], page)

def UploadPlayerPages():
    with open('data/players.json', 'r') as f:
        players = json.load(f)

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

UploadSeasonCupsESL()
# UploadCupMatchPagesESL()
# UploadTeamPages()
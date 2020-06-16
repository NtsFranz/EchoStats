import requests
import json
from string import Template
from datetime import datetime


#################
# Init Wiki
#################
WIKI = True
S = requests.Session()

URL = "http://localhost/mediawiki/api.php"

# Step 1: GET request to fetch login token
PARAMS_0 = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_0)
DATA = R.json()

LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: POST request to log in. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
PARAMS_1 = {
    "action": "login",
    "lgname": "vrml_scraper_bot",
    "lgpassword": "scraper23478237489",
    "lgtoken": LOGIN_TOKEN,
    "format": "json"
}

R = S.post(URL, data=PARAMS_1)

# Step 3: GET request to fetch CSRF token
PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_2)
DATA = R.json()

CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
################


table_header = '{| class="wikitable sortable"\n'
table_row = '|-\n'
table_footer = '|}\n'

def UploadSeasonCupsESL():
    # load the data into an object from file
    with open('data/ESL_NA.json') as f:
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
    with open('data/ESL_NA.json') as f:
        esl_data = json.load(f)

    for cup in esl_data['cups']:
        page = "This cup is a part of the VR Challenger League. See the [[VR Challenger League (ESL) List of Cups|full list of cups]].\n\n"

        page += "[" + cup['link'] + " ESL Cup Page]\n\n"

        page += "Number of teams in this cup: " + str(len(cup['teams'])) + "\n\n"

        if "registration" in cup['link']:
            page += "This cup is a registration cup, so it contains no matches.\n"
        else:
            page += "=== List of Matches ===\n"

            # Create the table string
            page += table_header
            page += table_row
            page += '! Time !! External Cup Page !! Home Team !! Home Team Score !! Away Team Score !! Away Team\n'
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


def createPage(pageName, pageData):
    # Step 4: POST request to edit a page
    PARAMS_3 = {
        "action": "edit",
        "title": pageName,
        "token": CSRF_TOKEN,
        "format": "json",
        "text": pageData
    }

    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()

    print(DATA)

#UploadSeasonCupsESL()
UploadCupMatchPagesESL()
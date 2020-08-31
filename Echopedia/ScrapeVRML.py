from WikiCommon import *
import LocalInternet

from pyquery import PyQuery as pq

baseURL = 'https://vrmasterleague.com'

def scrapeVRMLTeams():
    print("scrapeVRMLTeams")

    teams = loadJSON('teams')
    matches = loadJSON('matches')

    # loop through the seasons known
    for season_id, season in seasons_data.items():

        # skip esl seasons
        if season['api_type'] != 'vrml':
            continue

        # load the series rankings to get all the team names
        page = LocalInternet.local_pq(season['standings_url'])

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
                if 'old_team_names' not in team:
                    team['old_team_names'] = []
                old_team_name = team['team_name'].split(' (aka ')[0]
                if old_team_name not in team['old_team_names']:
                    team['old_team_names'].append(old_team_name)
                team['team_name'] = team['team_name'].split(' (aka ')[1][:-1]
                print('old name: ' + old_team_name)
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
            default_team_page = LocalInternet.local_pq(team['team_page'])

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
            team_page = pq(LocalInternet.get(team['team_page']))
            # success = False
            # while not success:
            #     try:
            #         team_page = pq(LocalInternet.get(team['team_page']))
            #         success = True
            #     except:
            #         print("Failed to load. Retrying...")
            

            roster = []
            if season_id == "vrml_season_2":
                past_roster = team_page('.players_container .player_name')
            else:
                past_roster = team_page(
                    '.teams_roster_season_container .player_name')

            for p in past_roster:
                roster.append(pq(p).text())
            team['roster'] = roster


            # get team bio and discord
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
                if len(match_pq('.score_cell').text().split(' ')) > 2:
                    match['teams'] = [
                        {
                            'team_id': match_pq('.home_team_cell > .team_link').attr('href').split('/')[-1],
                            'team_page': baseURL + match_pq('.home_team_cell > .team_link').attr('href'),
                            'team_logo': baseURL + match_pq('.home_team_cell > .team_link > .team_logo').attr('src'),
                            'team_name': match_pq('.home_team_cell').text(),
                            'score': match_pq('.score_cell').text().split(' ')[0],
                            'won': len(match_pq('.home_team_cell > .glyphicon-arrow-up')) > 0
                        },
                        {
                            'team_id': match_pq('.away_team_cell > .team_link').attr('href').split('/')[-1],
                            'team_page': baseURL + match_pq('.away_team_cell > .team_link').attr('href'),
                            'team_logo': baseURL + match_pq('.away_team_cell > .team_link > .team_logo').attr('src'),
                            'team_name': match_pq('.away_team_cell').text(),
                            'score': match_pq('.score_cell').text().split(' ')[2],
                            'won': len(match_pq('.away_team_cell > .glyphicon-arrow-up')) > 0
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

    dumpJSON('teams', teams)
    dumpJSON('matches', matches)


def scrapeVRMLPlayers():
    print("scrapeVRMLPlayers")

    players = loadJSON('players')

    for season_id, season in seasons_data.items():
        if season['api_type'] != 'vrml':
            continue

        page = LocalInternet.local_pq(season['players_url'])
        if season_id == 'vrml_season_2':
            numPlayers = int(page('.players-list-header-count').text()[20:23])
        else:
            numPlayers = int(page('.players-list-header-count').text()[0:4])

        for i in range(0, int(numPlayers/100)+1):
            page = LocalInternet.local_pq(season['players_url']+"?posMin="+str(i*100+1))

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
                if 'vrml_team' not in player:
                    player["vrml_team"] = {}
                player['vrml_team'][season_id] = {
                    "team_name": player_pq(
                    '.team_cell > a > span').text(),
                    "team_page": baseURL + \
                    player_pq('.team_cell > a').attr('href'),
                    "team_logo": baseURL + \
                    player_pq('.team_cell > a > img').attr('src')
                }
                nat_img_cell = player_pq('.nationality_cell > img')
                if nat_img_cell:
                    player['vrml_nationality'] = nat_img_cell.attr('title')
                    player['vrml_nationality_logo'] = baseURL + \
                        nat_img_cell.attr('src')
                else:
                    player['vrml_nationality'] = None
                    player['vrml_nationality_logo'] = None

    dumpJSON('players', players)


# only gets stats and rosters for the current season. This is faster than getting full stats
# This method forces actual network loading instead of LocalInternet caching
def scrapeCurrentSeasonTeamStats(season_name):

    forceRealInternet = True

    teams = loadJSON('teams')
    players = loadJSON('players')

    # loop through the players and get their teams
    print(seasons_data[season_name]['players_url'])
    page = pq(LocalInternet.get(seasons_data[season_name]['players_url'], forceRealInternet))

    if season_name == 'vrml_season_2':
        numPlayers = int(page('.players-list-header-count').text()[20:23])
    else:
        numPlayers = int(page('.players-list-header-count').text()[0:4])


    # load the team standing page
    another_page = True
    page_num = 0

    while another_page:
        print(seasons_data[season_name]['standings_url']+"?rankMin="+str(page_num*100+1))
        page = pq(LocalInternet.get(seasons_data[season_name]['standings_url']+"?rankMin="+str(page_num*100+1), forceRealInternet))
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
        url = seasons_data[season_name]['players_url']+"?posMin="+str(i*100+1)
        print(url)
        page = pq(LocalInternet.get(url, forceRealInternet))

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

    dumpJSON('teams', teams)
    dumpJSON('players', players)

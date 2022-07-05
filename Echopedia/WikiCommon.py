seasons_data = {
    'vrcl_s1': {
        'name': 'VR Challenger League Season 1',
        'wiki_page': 'VR Challenger League Season 1 (ESL)',
        'file': 'data/vrcl_s1_cups.json',
        'api_type': 'esl',
        'api_urls': {
            'na': 'https://api.eslgaming.com/play/v1/leagues?types=a_series,cup,esl_series,ladder,premiership,swiss&states=finished&tags=&path=/play/echoarena/north-america/&includeHidden=0&skill_levels=pro_qualifier,open,pro,major&limit.total=5000',
            'eu': 'https://api.eslgaming.com/play/v1/leagues?types=a_series,cup,esl_series,ladder,premiership,swiss&states=finished&tags=&path=/play/echoarena/europe/&includeHidden=0&skill_levels=pro_qualifier,open,pro,major&limit.total=5000'
        }
    },
    'vrl_s2': {
        'name': 'VR League Season 2',
        'wiki_page': 'VR League Season 2 (ESL)',
        'file': 'data/vrl_s2_cups.json',
        'api_type': 'esl',
        'api_urls': {
            'na': 'https://api.eslgaming.com/play/v1/leagues?types=swiss&states=finished&tags=vrlechoarena-na-portal&path=/play/&includeHidden=0&skill_levels=major&limit.total=40000',
            'eu': 'https://api.eslgaming.com/play/v1/leagues?types=swiss&states=finished&tags=vrlechoarena-eu-portal&path=/play/&includeHidden=0&skill_levels=major&limit.total=40000'
        }
    },
    'vrl_s3': {
        'name': 'VR League Season 3',
        'wiki_page': 'VR League Season 3 (ESL)',
        'file': 'data/vrl_s3_cups.json',
        'api_type': 'esl',
        'api_urls': {
            'na': 'https://api.eslgaming.com/play/v1/leagues?types=swiss&states=finished&tags=vrlechoarena-na-portal&path=/play/&includeHidden=0&skill_levels=major&limit.total=40000',
            'eu': 'https://api.eslgaming.com/play/v1/leagues?types=swiss&states=finished&tags=vrlechoarena-eu-portal&path=/play/&includeHidden=0&skill_levels=major&limit.total=40000'
        }
    },
    'vrml_preseason': {
        'name': 'VR Master League Pre-season',
        'wiki_page': 'VR Master League (VRML) Pre-season 2019',
        'dropdown_name': 'Pre-season - 2019 (history)',
        'file': 'data/vrml_preseason.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090?season=b-VHi9XjGIR0Pv17C7P_Tw2',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players?season=b-VHi9XjGIR0Pv17C7P_Tw2'
    },
    'vrml_season_1': {
        'name': 'VR Master League Season 1',
        'wiki_page': 'VR Master League (VRML) Season 1 2020',
        'dropdown_name': 'Season 1 - 2020 (history)',
        'file': 'data/vrml_s1.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090?season=PS5eV-VOdnRPCAxRix9xlQ2',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players?season=PS5eV-VOdnRPCAxRix9xlQ2'
    },
    'vrml_season_2': {
        'name': 'VR Master League Season 2',
        'wiki_page': 'VR Master League (VRML) Season 2 2020',
        'dropdown_name': 'Season 2 - 2020 (history)',
        'file': 'data/vrml_s2.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090?season=NLQNdfR3j0lyy6eLpLhIYw2',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players?season=NLQNdfR3j0lyy6eLpLhIYw2'
    },
    'vrml_season_3': {
        'name': 'VR Master League Season 3',
        'wiki_page': 'VR Master League (VRML) Season 3 2021',
        'dropdown_name': 'Season 3 - 2021 (history)',
        'file': 'data/vrml_s3.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090?season=XPtJ0s7XBpsbDHrjS0e_3g2',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players?season=XPtJ0s7XBpsbDHrjS0e_3g2'
    },
    'vrml_season_4': {
        'name': 'VR Master League Season 4',
        'wiki_page': 'VR Master League (VRML) Season 4 2021',
        'dropdown_name': 'Season 4 - 2021 (history)',
        'file': 'data/vrml_s4.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090?season=YJoYnb3iWN8EcCrs92U04A2',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players?season=YJoYnb3iWN8EcCrs92U04A2'
    },
    'vrml_season_5': {
        'name': 'VR Master League Season 5',
        'wiki_page': 'VR Master League (VRML) Season 5 2022',
        'dropdown_name': 'Season 5 - 2022',
        'file': 'data/vrml_s5.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090?season=XKVgWTi5AdpkSQnLhhs7bw2',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players?season=XKVgWTi5AdpkSQnLhhs7bw2'
    },
}

import os
import json

def loadJSON(filename: str) -> dict:
    path = os.path.join(os.path.dirname(__file__), 'data/'+filename+'.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        return {}

def dumpJSON(filename: str, data: dict):
    path = os.path.join(os.path.dirname(__file__), 'data/'+filename+'.json')
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
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
        'file': 'data/vrml_preseason.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnJNSzVPMG9XcTlLdz090',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players/List/U3ZUS2g0NkdkZjg90'
    },
    'vrml_season_1': {
        'name': 'VR Master League Season 1',
        'wiki_page': 'VR Master League (VRML) Season 1 2020',
        'file': 'data/vrml_s1.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/SnE5TUFtaWRJZnFoQitjQjFjYlBXZz090',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players/List/c2VkWExsOERkSmc90'
    },
    'vrml_season_2': {
        'name': 'VR Master League Season 2',
        'wiki_page': 'VR Master League (VRML) Season 2 2020',
        'file': 'data/vrml_s2.json',
        'api_type': 'vrml',
        'standings_url': 'https://vrmasterleague.com/EchoArena/Standings/d3JZU1F5WlVraGc90',
        'players_url': 'https://vrmasterleague.com/EchoArena/Players/List/bnpWeFFsakNtTjA90'
    }
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
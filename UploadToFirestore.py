import datetime
import json
import os
from pathlib import Path

import firebase_admin
import requests
from firebase_admin import credentials, firestore
from google.cloud import storage
from pyquery import PyQuery as pq

#################
# Init Firestore
#################
FIREBASE = False
project_id="ignitevr-echostats"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ignitevr-echostats-firebase-adminsdk-nzhes-c287edff87.json"

# Use the application default credentials
#cred = credentials.Certificate("ignitevr-echostats-firebase-adminsdk-nzhes-c287edff87.json")
#cred = credentials.Certificate("ignitevr-echostats-9e1d8f70c8a0.json")
cred = credentials.Certificate("ignitevr-echostats-firebase-adminsdk-nzhes-1424f20b2b.json")
firebase_admin.initialize_app(cred, { 'projectId': project_id })
#firebase_admin.get_app()

db = firestore.client()

def upload_esl_data():
    with open('data/VRL_S3_cups.json') as f:
        esl_data = json.load(f)
    
    for cup in esl_data['cups']:
        cup_doc_ref = db.collection('series/esl_season_3/cups').document(str(cup['id']))

        batch = db.batch()
        for team in cup['teams']:
            team_doc_ref = cup_doc_ref.collection('teams').document(str(team['id']))
            batch.set(team_doc_ref, team)
        del cup['teams']

        for match in cup['matches']:
            match_doc_ref = cup_doc_ref.collection('matches').document(str(match['id']))
            for team in match['teams']:
                team_doc_ref = match_doc_ref.collection('teams').document(str(team['id']))
                batch.set(team_doc_ref, team)
            del match['teams']
            batch.set(match_doc_ref, match)
        del cup['matches']

        batch.set(cup_doc_ref, cup)
        batch.commit()
    



    batch = db.batch()
    for team in esl_data['teams'].items():
        teams_doc_ref = db.collection('series/esl_season_3/teams').document(str(team[0]))

        for member in team[1]['roster']:
            member_doc_ref = teams_doc_ref.collection('roster').document(str(member['id']))
            batch.set(member_doc_ref, member)
        del team[1]['roster']

        batch.set(teams_doc_ref, team[1])

    batch.commit()


upload_esl_data()
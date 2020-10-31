# ping graph
# by NtsFranz
# .echoreplay file loading inspired by Graic: https://github.com/Graicc/RePlaySpace-Abuse-Detector/

import zipfile
import os
import sys
import tempfile
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import datetime
format = r'%Y/%m/%d %H:%M:%S.%f'


# extracts the JSON object and the timestamp from a .echoreplay line
def get_frame(line: str):
    timestamp, jsondata = line.split("\t")
    return datetime.datetime.strptime(timestamp, format), json.loads(jsondata)


# finds the player object with the given name or returns None
def get_player(json: str, player_name: str):
    for team in json['teams']:
        if 'players' in team:
            for player in team['players']:
                if player['name'] == player_name:
                    return player
    return None


def get_all_players(json: str) -> []:
    players_list = []
    for team in json['teams']:
        if 'players' in team:
            for player in team['players']:
                if player['name'] not in players_list:
                    players_list.append(player['name'])
    return players_list

# ping graph

filepath = sys.argv[1]

# exctract the .echoreplay file
data = []
if zipfile.is_zipfile(filepath):
    # Unzip
    with zipfile.ZipFile(filepath, 'r') as zf:
        with tempfile.TemporaryDirectory() as td:
            zf.extractall(td)
            for entry in os.scandir(td):
                with open(entry.path, 'r') as f:
                    data = f.readlines()
else:
    with open(filepath) as f:
        data = f.readlines()

print("Loaded file into memory ({0} lines)".format(len(data)))

print("Processing frames...")
json_lines = [get_frame(line)[1] for line in data if len(line) > 800]

players_list = set([])
skip_rate = 100
for i in range(0, int(len(json_lines)/skip_rate)):
    for p in get_all_players(json_lines[i*skip_rate]):
        players_list.add(p)

print('Players in this replay:')
players_list = list(players_list)
for i in range(0, len(players_list)):
    print("{0}) {1}".format(i, players_list[i]))

choice = int(input(
    'Choose a player to PING GRAPH (0, {0}): '.format(len(players_list)-1)))
player_name = players_list[choice]

players = []
for line in data:
    if len(line) > 800:
        p = get_player(get_frame(line)[1], player_name)
        if p is not None:
            players.append(p)
            
df = pd.DataFrame(players)
df = df[['ping', 'possession']]
df['x'] = df.index
print("Found player in {0} frames.".format(len(df)))

# distribution differences
sns.displot(df, x='ping', hue='possession', kind='kde')

# ping graph

# time series
df['ping_no_possession'] = df['ping']
df['ping_possession'] = df['ping']

df.loc[df['possession'] == True, 'ping_no_possession'] = None
df.loc[df['possession'] == False, 'ping_possession'] = None

# ping graph

fig, ax = plt.subplots(figsize=(30, 10))

df.plot(ax=ax, x="x", y="ping_no_possession", label="False", color='C0')
df.plot(ax=ax, x="x", y="ping_possession", label="True", color='C1')

# ping graph

ax.set_xticklabels([])

plt.show()


# ping graph
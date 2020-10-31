# by NtsFranz
# .echoreplay file loading inspired by Graic: https://github.com/Graicc/RePlaySpace-Abuse-Detector/

import zipfile
import os
import sys
import tempfile
import json
# import seaborn as sns
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


folder = sys.argv[1]
count = sys.argv[2]

files = os.listdir(folder)
files = files[len(files)-int(count):]

# exctract the .echoreplay file
data = []
for f in files:
    filepath = os.path.join(folder, f)
    print("Loading file into memory: {0}".format(f))
    if zipfile.is_zipfile(filepath):
        # Unzip
        with zipfile.ZipFile(filepath, 'r') as zf:
            with tempfile.TemporaryDirectory() as td:
                zf.extractall(td)
                for entry in os.scandir(td):
                    with open(entry.path, 'r') as f:
                        data.extend(f.readlines())
    else:
        with open(filepath) as f:
            data.extend(f.readlines())

print("Loaded file into memory ({0} lines)".format(len(data)))

print("Processing frames...")
skip_factor = 80
json_lines = []
for i in range(0, len(data)):
    if i % skip_factor == 0 and len(data[i]) > 800:
        json_lines.append(get_frame(data[i])[1])
        print(".", end='')

print("")
print("Processed {0} frames".format(len(json_lines)))

print("Processing frames again...")
scores = []
for line in json_lines:
    print(".", end='')
    scores.append({
        "game_clock": line['game_clock'] / 100,
        "blue": line['blue_points'],
        "orange": line['orange_points']
    })

df = pd.DataFrame(scores)
# df = df[['ping', 'possession']]
df['x'] = df.index


fig, ax = plt.subplots(figsize=(20, 10))

df.plot(ax=ax, x="x", y="blue", label="Synapse", color='C0')
df.plot(ax=ax, x="x", y="orange", label="Ignite", color='C1')
df.plot(ax=ax, x="x", y="game_clock", label="Game Clock", color='C2')

ax.set_xticklabels([])

plt.show()

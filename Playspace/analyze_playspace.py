from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import sqlite3
import requests
import tempfile
import zipfile
import os
import datetime
import json
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.patches as patches
import plotly.graph_objects as go
import numpy as np
fmt = r'%Y/%m/%d %H:%M:%S.%f'

"""
# Playspace Visualization
### Analyzes a .echoreplay clip to see how much playspace abuse there is
  \- Created by NtsFranz
"""


replay_file_buffer = st.file_uploader(
    "Upload a .echoreplay file", type=["echoreplay"])
data = []

if replay_file_buffer is not None:

    if zipfile.is_zipfile(replay_file_buffer):
        # Unzip
        with zipfile.ZipFile(replay_file_buffer, 'r') as zf:
            with tempfile.TemporaryDirectory() as td:
                zf.extractall(td)
                for entry in os.scandir(td):
                    with open(entry.path, 'r') as f:
                        data.extend(f.readlines())
    else:
        with open(replay_file_buffer) as f:
            data.extend(f.readlines())

    st.text("Loaded file into memory ({0} lines)".format(len(data)))

    # extracts the JSON object and the timestamp from a .echoreplay line

    def get_frame(line: str):
        timestamp, jsondata = line.split("\t")
        return datetime.datetime.strptime(timestamp, fmt), json.loads(jsondata)

    # finds the player object with the given name or returns None

    def get_player(json: str, player_name: str):
        for team in json['teams']:
            if 'players' in team:
                for player in team['players']:
                    if player['name'] == player_name:
                        player['game_clock'] = json['game_clock']
                        return player
        return None

    xyz = ['x', 'y', 'z']
    # converts the list of raw replay lines to a list of frames
    frames = [get_frame(line)[1] for line in data if len(line) > 800]
    print("Loaded JSON frames...")

    # adds x,y,z of local player position to the list and puts into a dict to load into dataframe
    players = [{xyz[i]: frame['player']['vr_position'][i]
                for i in range(0, 3)} | frame for frame in frames]
    rawDF = pd.DataFrame(players)
    rawDF

    # graph the positions in a heatmap
    colormap = 'jet'
    figscale = 1
    r = 1
    plt.rcParams.update({'font.size': 20})
    # params = {"ytick.color" : "w",
    #         "xtick.color" : "w",
    #         "text.color" : "w",
    #         "axes.labelcolor" : "w",
    #         "axes.edgecolor" : "w"}
    # plt.rcParams.update(params)

    df = rawDF

    fig, (ax1, ax2) = plt.subplots(
        1, 2, tight_layout=True, figsize=(20*figscale, 10*figscale))
    # fig.patch.set_visible(False)
    # ax.axis('off')
    hist = ax1.hist2d(df['x'], df['z'],
                      bins=(100, 100),
                      range=[[-r, r], [-r, r]],
                      norm=colors.LogNorm(), cmap=colormap)

    hist = ax2.hist2d(df['x'], df['y'],
                      bins=(100, 100),
                      range=[[-r, r], [-r, r]],
                      norm=colors.LogNorm(), cmap=colormap)

    # ft to meters conversion
    fourFT = 1.2192
    rect1 = patches.Rectangle((-fourFT/2, -fourFT/2), fourFT,
                              fourFT, linewidth=1, edgecolor='r', facecolor='none')
    rect2 = patches.Rectangle((-fourFT/2, -1), fourFT,
                              2, linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    ax1.add_patch(rect1)
    ax2.add_patch(rect2)
    # plt.axis('off')
    # plt.show()

    # fig.suptitle('2D Histogram of playspace positions. Red box is 4ftx4ft.')
    st.subheader(
        '2D Histogram of local playspace head positions. Red box is 4ftx4ft.')
    'This uses the local playspace location, so it is accurate (barring tracking issues). The positions are recentered based on the average position, since not all players have their Oculus playspace bounds set correctly'
    'This is head position, so some deviation outside the bounds would be acceptable under the rules.'
    ax1.set_title('Top View')
    ax2.set_title('Side View')

    st.pyplot(fig)
    # plt.savefig('playspace_top_side.png')

    # st.subheader(
    #     'Line showing local playspace head positions over time. Red box is 4ftx4ft.')
    # sliderval = st.slider('Time', min_value=0, max_value=len(df))
    # plt.rcParams.update({'font.size': 10})
    # fig, ax = plt.subplots(1, figsize=(5, 5))
    # ax.axis([-1, 1, -1, 1])
    # ax.plot(df['x'][:sliderval], df['y']
    #         [:sliderval], linewidth=2, color='#c44')
    # st.pyplot(fig)

    N = 50
    zero_pt = pd.Series([0])
    r = fourFT/2
    bottom = df['z'].min()
    z = zero_pt.append(df['x'], ignore_index = True).reset_index(drop = True)
    y = zero_pt.append(df['y'], ignore_index = True).reset_index(drop = True)
    x = zero_pt.append(df['z'], ignore_index = True).reset_index(drop = True)
    fig = go.Figure(data=[
        go.Scatter3d(x=df['x'], y=df['z'], z=df['y'],
            marker=dict(
                size=2,
                color=df['game_clock'],
                colorscale='Hot',
            ),
            name='Head Position'
        ),
        # go.Scatter3d(x=[-1, 1, 1, -1, -1, -1], y=[-1, -1, -1, -1], z=[-1, -1, 1, 1])
        go.Scatter3d(x=[-r, r, r, -r, -r], y=[r, r, -r, -r, r], z=[bottom, bottom, bottom, bottom, bottom], name='4ft x 4ft'),
        # go.Scatter3d(x=[-r, r, r, -r, -r], y=[r, r, -r, -r, r], z=[0, 0, 0, 0, 0]),
    ]
    )
    fig.update_layout(title='Local Playspace Head Positions',
                      height=800,
                      scene=dict(
                          #   aspectratio=dict(x=1, y=1, z=1),
                        #   aspectmode='manual'
                      ),)
    st.plotly_chart(fig)

    # # animated plot
    # import matplotlib.animation as animation
    # import numpy as np
    # plt.rcParams.update({'font.size': 10})
    # fig, ax = plt.subplots(1, figsize=(5, 5))

    # line, = ax.plot(df['x'], df['y'], linewidth=2, color='#c44')

    # def init():  # only required for blitting to give a clean slate.
    #     line.set_ydata([np.nan] * len(df['y']))
    #     return line,

    # def update(num, x, y, line):
    #     line.set_data(x[:num], y[:num])
    #     line.axes.axis([-1, 1, -1, 1])
    #     return line,

    # ani = animation.FuncAnimation(fig, update, len(
    #     df), fargs=[df['x'], df['y'], line], interval=33, blit=True)
    # ani.save('test.gif')
    # st.pyplot(fig)

    # st.subheader(
    #     'Line showing local playspace head positions over time. Red box is 4ftx4ft.')
    # chart = alt.Chart(df).mark_trail().encode(x='x', y='y')
    # st.altair_chart(chart)

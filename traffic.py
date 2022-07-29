
# Importing the needed libraries

import requests
import pandas as pd
import json
from tqdm import tqdm
from statistics import *
import sqlite3
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML, fromstring, tostring
import time as t
from datetime import *


# Defining the parameters for Milan

here_api_key = "j5prxmqI5FlbeCTfsoGOsNPeBL5s_u22d-tNf-0I5ec"

# Milan center coordinates and radius
MI_lat = '45.464664'
MI_lon = '9.188540'
MI_south = '9.0525169'
MI_west = '45.3933901'
MI_north = '9.2727576'
MI_east = '45.5351523'
rad = '20000'


# Creating a connection with the SQL database

conn = sqlite3.connect('traffic.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE traffic_table (
    date_time DATETIME,
    name TEXT,
    lat TEXT,
    lon TEXT,
    length TEXT,
    actual_speed FLOAT,
    free_flow speed FLOAT,
    jam_factor FLOAT,
    traversability TEXT)''')


def get_traffic():
    # Getting the data
    traffic_url = 'https://data.traffic.hereapi.com/v7/flow?apiKey='+here_api_key+'&in=circle:'+MI_lat+','+MI_lon+';r='+rad+'&locationReferencing=shape'
    data = requests.get(traffic_url).json()

    # Defining the time
    time_traffic = data['sourceUpdated'].replace('T', ' ').replace('Z', '')
    datetime_traffic = datetime.strptime(time_traffic, '%Y-%m-%d %H:%M:%S')

    # Defining the other info
    location = []
    lat = []
    lon = []
    length = []
    currentSpeed = []
    freeFlowSpeed = []
    jamFactor = []
    traversability = []
    for res in data['results']:
        floc = res['location']
        if 'description' in floc.keys():
            loc_name = str(floc['description'])
        else:
            loc_name = 'Unknown location'
        if 'length' in floc.keys():
            loc_len = str(floc['length'])
        else:
            loc_len = 'Unknown length'
        lats = []
        lngs = []
        for link in floc['shape']['links']:
            # print(link['points'])
            lat_list = [p['lat'] for p in link['points']]
            #print(lat_list)
            for lt in lat_list:
                lats.append(lt)
            lng_list = [p['lng'] for p in link['points']]
            #print(lng_list)
            for lg in lng_list:
                lngs.append(lg)

        fcF = res['currentFlow']
        if ('speed' in fcF.keys()) and ('freeFlow' in fcF.keys()) and ('traversability' in fcF.keys()) and ('jamFactor' in fcF.keys()):
            act_sp = float(fcF['speed']*3.6)
            ff_sp = float(fcF['freeFlow']*3.6)
            jam_f = float(fcF['jamFactor'])
            travers = str(fcF['traversability'])
        else:
            continue

        location.append(loc_name)
        length.append(loc_len)
        currentSpeed.append(act_sp)
        freeFlowSpeed.append(ff_sp)
        jamFactor.append(jam_f)
        traversability.append(travers)
        lat.append(lats)
        lon.append(lngs)

    def_traffic = pd.DataFrame(list(zip(location, length, lat, lon, currentSpeed, freeFlowSpeed, jamFactor, traversability)), columns=['name', 'length', 'lat', 'lon', 'actual_speed', 'free_flow_speed', 'jam_factor', 'traversability'])

    # Adding the 'date_time' column
    def_traffic['date_time'] = datetime_traffic

    # Normalizing the 'jam_factor' between 0 and 1
    jam_norm = round((def_traffic['jam_factor']-def_traffic['jam_factor'].min())/(def_traffic['jam_factor'].max()-def_traffic['jam_factor'].min()), 2)
    redef_traffic = def_traffic.drop(columns='jam_factor')
    traffic_def = pd.concat((jam_norm, redef_traffic), 1)

    # Reordering the dataframe
    traffic_def = traffic_def[['date_time', 'name', 'length', 'lat', 'lon', 'actual_speed', 'free_flow_speed', 'jam_factor', 'traversability']]

    return traffic_def


# Running the infinite loop

while True:
    traffic_df = get_traffic()
    for row in traffic_df.iterrows():
        new_row = list(row[1])
        flow = [("date_time", new_row[0].to_pydatetime()),
        ("name", new_row[1]),
        ("length", new_row[2]),
        ("lat", repr(new_row[3])),
        ("lon", repr(new_row[4])),
        ("actual_speed", new_row[5]),
        ("free_flow_speed", new_row[6]),
        ("jam_factor", new_row[7]),
        ("traversability", new_row[8])]
        cursor.execute('INSERT INTO traffic_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', list(map(lambda x: x[1], flow)))

    now = datetime.now()
    print(traffic_df.head())
    print(f'Last update: {now}')

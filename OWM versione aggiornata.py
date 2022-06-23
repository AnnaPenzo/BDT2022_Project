#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 11:32:30 2022

@author: annapenzo
"""


import requests
import math
import sqlite3
import time

city_name = "Milan,IT"
api_key = "bcbd3c98dce9c884ca136388c89d3073"



#%%
conn = sqlite3.connect('meteo.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE weather (
    date_time INTEGER,
    weather TEXT,
    temperature INTEGER,
    temp_min INTEGER,
    temp_max INTEGER,
    feels_like INTEGER,
    humidity INTEGER,
    wind_speed REAL)''')
#cursor.execute(UPDATE weather)
#%%

def get_weather(api_key, city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&&appid={api_key}"
    
    response = requests.get(url).json()
    
    date_time = response["dt"]
    weather = response["weather"][0]["description"]
    temp = int(response["main"]["temp"]) - 273
    feels_like = int(response["main"]["feels_like"]) - 273
    temp_min = int(response["main"]["temp_min"]) - 273
    temp_max = int(response["main"]["temp_max"]) - 273
    humidity = response["main"]["humidity"]
    wind_speed = response["wind"]["speed"]
    
    
    return [("date_time", date_time),
            ("weather", weather),
            ("temperature", temp),
            ("temp_min", temp_min),
            ("temp_max", temp_max),
            ("feels_like", feels_like),
            ("humidity", humidity),
            ("wind_speed", wind_speed)]
    
#for x in range (0, 5): #my_impl  
weather = get_weather(api_key, city_name)
    #time.sleep(10) #my impl
cursor.execute('INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?)', list(map(lambda x: x[1], weather)))

print(weather)
conn.commit()

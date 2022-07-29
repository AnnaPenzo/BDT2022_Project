#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:52 2022

@author: annapenzo
"""

import sqlite3

def fetch_records(conn):
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM weather")

    rows = cur.fetchall()

    for row in rows:
        print(row) #here you can select the columns to display
        
conn = sqlite3.connect('meteo.db')
fetch_records(conn)

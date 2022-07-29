
import sqlite3

def fetch_records(conn):
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM weather")

    rows = cur.fetchall()

    for row in rows:
        print(row) #here you can select the columns to display
        
conn = sqlite3.connect('meteo.db')
fetch_records(conn)

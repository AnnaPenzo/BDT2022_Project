
import sqlite3
import matplotlib.pyplot as plt
import csv


def fetch_records(conn):
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM weather")

    rows = cur.fetchall()
    
    date_time = []
    weather = []
    temp = []
    feels_like = []
    temp_min = []
    temp_max = []
    humidity = []
    wind_speed = []
    
    
    for row in rows:
        date_time.append(row[0])
        weather.append(row[1])
        temp.append(row[2])
        feels_like.append(row[3])
        temp_min.append(row[4])
        temp_max.append(row[5])
        humidity.append(row[6])
        wind_speed.append(row[7])
        
    # Show the data 
    #print(date_time)
    #print(humidity)
    
    # Plot the data using a barplot
    plt.bar(weather, humidity, 0.5)
    plt.xlabel("Weather")
    plt.ylabel("Humidity")
    plt.title("Weather-humidity correlation")
    
    plt.show()
    
    # Save the data as a csv file
    with open("Weather_data", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["date_time", " weather", " temp", " feels_like", " temp_min", " temp_max", " humidity", " wind_speed"])
        csv_writer.writerows(rows)


conn = sqlite3.connect('meteo.db')
fetch_records(conn)

#!/usr/bin/env python3
import os
import requests
import pymysql
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  #

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    print("OPENWEATHER_API_KEY not found .env!")
    exit(1)

URL = f"https://api.openweathermap.org/data/2.5/weather?q=Oulu&appid={API_KEY}&units=metric"

conn = pymysql.connect(
    host="localhost",
    user="weather_user",
    password="4Rg5!33tt",
    database="weather_db",
    charset="utf8mb4"
)

cur = conn.cursor()

cur.execute("""
    INSERT INTO weather_data (city, temperature, feels_like, humidity, description)
    VALUES (%s, %s, %s, %s, %s)
""", (
    "Oulu",
    requests.get(URL).json()["main"]["temp"],
    requests.get(URL).json()["main"]["feels_like"],
    requests.get(URL).json()["main"]["humidity"],
    requests.get(URL).json()["weather"][0]["description"]
))

conn.commit()
print(f"{datetime.now()} → Oulu: the weather is written down")
cur.close()
conn.close()

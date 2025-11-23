#!/usr/bin/env python3
import requests
import pymysql
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("EXCHANGERATE_API_KEY")
if not API_KEY:
    print("EXCHANGERATE_API_KEY not found!")
    exit(1)

URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/EUR"

conn = pymysql.connect(
    host="localhost",
    user="weather_user",
    password=os.getenv("DB_PASS"),
    database="weather_db",
    charset="utf8mb4"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS currency_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nok_rate FLOAT,
    dkk_rate FLOAT,
    sek_rate FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

try:
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    if data.get("result") != "success":
        raise Exception(data.get("error-type", "API error"))

    rates = data["conversion_rates"]
    cur.execute("INSERT INTO currency_rates (nok_rate, dkk_rate, sek_rate) VALUES (%s, %s, %s)",
                (rates["NOK"], rates["DKK"], rates["SEK"]))
    conn.commit()
    print(f"{datetime.now():%Y-%m-%d %H:%M} → 1€ = {rates['NOK']:.3f} NOK | {rates['DKK']:.3f} DKK | {rates['SEK']:.3f} SEK")

except Exception as e:
    print(f"Error: {e}")
finally:
    cur.close()
    conn.close()

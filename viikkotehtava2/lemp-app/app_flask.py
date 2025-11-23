from flask import Flask
import mysql.connector
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="lempuser",
        password=os.getenv("LEMP_DB_PASS")
        database="lempdb"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();") 
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    # Convert MySQL UTC time to Helsinki time (UTC+2 or +3 with DST)
    utc_time = result[0]
    helsinki_time = utc_time + timedelta(hours=2)

    # HTML page
    html = f"""
    <html>
        <head>
            <title>My LEMP Stack App</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #ffe6f2;
                    text-align: center;
                    color: #333;
                    margin-top: 10%;
                }}
            </style>
        </head>
        <body>
            <h1>✨ Tervetuloa minun LEMP Stackille ✨</h1>

            <p>Server time from SQL (Helsinki): <b>{helsinki_time.strftime("%Y-%m-%d %H:%M:%S")}</b></p>

            <p><a href="/data-analysis/">(VIIKKOTEHTÄVÄ 3) TÄSTÄ pääset  Data Analysis</a></p>

        </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

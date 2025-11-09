from flask import Flask
import mysql.connector

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Connect to MySQL/MariaDB
    conn = mysql.connector.connect(
        host="localhost",
        user="lempuser",               # Replace with your DB username
        password="f#r579Ddq", # Replace with your DB password
        database="lempdb"              # Replace with your DB name
    )

    cursor = conn.cursor()
    # Fetch current time from SQL server
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()

    # Clean up database connection
    cursor.close()
    conn.close()

    # Build HTML page
    html = f"""
    <html>
        <head>
            <title>My LEMP Stack App</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #ffe6f0; /* Light pink background */
                    text-align: center;
                    color: #333;
                    margin-top: 5%;
                }}
                h1 {{
                    font-size: 2.5em;
                    color: #d63384;
                    margin-bottom: 20px;
                }}
                .time {{
                    font-weight: bold;
                    color: #e60073;
                    font-size: 1.2em;
                }}
            </style>
        </head>
        <body>
            <!-- Personalized greeting with emoji -->
            <h1>✨ Tervetuloa My LEMP Stackille ✨</h1>
            <!-- Server time from SQL -->
            <p>Server time from SQL: <span class="time">{result[0]}</span></p>
        </body>
    </html>
    """
    return html

if __name__ == '__main__':
    # Run the Flask app on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)

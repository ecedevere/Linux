import streamlit as st
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()

def load_pulse24h():
    conn = MySQLdb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASS"),
        db=os.getenv("DB_NAME")
    )
    df = pd.read_sql("SELECT * FROM pulse24h ORDER BY timestamp", conn)
    conn.close()
    return df

st.title("❤️ Pulssi 24H ❤️")

df = load_pulse24h()

st.line_chart(df[['pulse']])
st.dataframe(df)

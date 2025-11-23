import streamlit as st
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from dotenv import load_dotenv
import os
from datetime import datetime

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

# Weather Oulu
st.markdown("---")
st.title("❄️Sää Oulussa❄️")
st.markdown("*(päivittyy 15 min välein)*")

try:
    conn = pymysql.connect(
        host="localhost",
        user="weather_user",
        password="4Rg5!33tt",
        database="weather_db",
        charset="utf8mb4"
    )

    dfw = pd.read_sql("""
        SELECT timestamp, temperature, feels_like, humidity, description 
        FROM weather_data 
        ORDER BY timestamp DESC LIMIT 20
    """, conn)

    dfw['timestamp'] = pd.to_datetime(dfw['timestamp'])

    display_df = dfw.copy()
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%H:%M %d.%m.')
    display_df.columns = ["Aika", "Lämpötila °C", "Tuntuu °C", "Kosteus %", "Kuvaus"]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Aika": st.column_config.TextColumn(width="small"),
                "Lämpötila °C": st.column_config.NumberColumn(format="%.1f"),
                "Tuntuu °C": st.column_config.NumberColumn(format="%.1f"),
                "Kosteus %": st.column_config.NumberColumn(format="%d"),
                "Kuvaus": st.column_config.TextColumn(width="medium")
            }
        )

    with col2:
        latest = dfw.iloc[0]
        st.metric("Lämpötila", f"{latest['temperature']:.1f} °C")
        st.metric("Tuntuu kuin", f"{latest['feels_like']:.1f} °C")
        st.metric("Kosteus", f"{latest['humidity']} %")
        st.markdown(f"**{latest['description'].capitalize()}**")

    st.subheader("Lämpötilan kehitys")
    st.line_chart(dfw.set_index('timestamp')['temperature'], use_container_width=True)

    st.caption(f"Viimeksi päivitetty: {datetime.now().strftime('%d.%m.%Y %H:%M')} • OpenWeatherMap")

    conn.close()

except Exception as e:
    st.info("Säädataa ladataan...")



#valuutta
st.markdown("---")
st.title("💰Valuuttakurssit (1 €)💰")
st.markdown("*(päivittyy 15 min välein)*")

try:
    conn = pymysql.connect(host="localhost", user="weather_user", password="4Rg5!33tt", database="weather_db", charset="utf8mb4")
    
    dfc = pd.read_sql("""
        SELECT timestamp, 
               nok_rate AS "NOK (Norja)", 
               dkk_rate AS "DKK (Tanska)", 
               sek_rate AS "SEK (Ruotsi)"
        FROM currency_rates 
        ORDER BY timestamp DESC LIMIT 20
    """, conn)
    
    dfc['timestamp'] = pd.to_datetime(dfc['timestamp'])

    col1, col2 = st.columns([3, 1])

    with col1:
        st.dataframe(dfc.style.format({
            "timestamp": "{:%H:%M %d.%m.%Y}",
            "NOK (Norja)": "{:.3f}",
            "DKK (Tanska)": "{:.3f}",
            "SEK (Ruotsi)": "{:.3f}"
        }), use_container_width=True, hide_index=True)

    with col2:
        latest = dfc.iloc[0]
        st.metric("EUR → NOK", f"{latest['NOK (Norja)']:.3f}")
        st.metric("EUR → DKK", f"{latest['DKK (Tanska)']:.3f}")
        st.metric("EUR → SEK", f"{latest['SEK (Ruotsi)']:.3f}")

    st.subheader("Kurssien kehitys")
    st.line_chart(dfc.set_index('timestamp')[["NOK (Norja)", "DKK (Tanska)", "SEK (Ruotsi)"]], use_container_width=True)

    st.caption(f"Viimeksi päivitetty: {datetime.now().strftime('%d.%m.%Y %H:%M')} • exchangerate-api.com")

    conn.close()

except Exception as e:
    st.info("Valuuttadataa ladataan vielä – odota ensimmäistä cron-ajoa (max 15 min)")

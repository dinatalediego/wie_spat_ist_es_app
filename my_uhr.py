import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pytz

class ClockPlot:
    def __init__(self, hour, minute):
        self.hour = hour % 12
        self.minute = minute

    def draw_clock(self):
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis("off")

        clock_face = plt.Circle((0, 0), 1, color='lightgrey', fill=True)
        ax.add_patch(clock_face)

        for i in range(1, 13):
            angle = np.pi/2 - 2*np.pi * (i / 12)
            ax.text(np.cos(angle)*0.85, np.sin(angle)*0.85, str(i),
                    ha='center', va='center', fontsize=10)

        angle_min = np.pi/2 - 2*np.pi * (self.minute / 60)
        ax.plot([0, np.cos(angle_min)*0.9], [0, np.sin(angle_min)*0.9], lw=2, color='blue')

        angle_hour = np.pi/2 - 2*np.pi * ((self.hour + self.minute/60) / 12)
        ax.plot([0, np.cos(angle_hour)*0.6], [0, np.sin(angle_hour)*0.6], lw=3, color='black')

        return fig

# Diccionario de frases cotidianas con sus horas
examples = {
    "fünf nach elf": (11, 5),
    "zehn nach drei": (3, 10),
    "Viertel nach zehn": (10, 15),
    "20 nach sechs": (6, 20),
    "fünf vor halb acht": (7, 25),
    "halb zwei": (1, 30),
    "fünf nach halb eins": (12, 35),
    "halb drei": (2, 30),
    "fünf vor drei": (2, 55)
}

# Ciudades por zona horaria común (simplificada)
city_timezones = {
    "Europe/Berlin": "Berlin",
    "America/New_York": "New York",
    "Asia/Tokyo": "Tokyo",
    "America/Lima": "Lima",
    "Europe/London": "London",
    "Australia/Sydney": "Sydney",
    "Asia/Dubai": "Dubai",
    "Africa/Johannesburg": "Johannesburg",
    "America/Mexico_City": "Ciudad de México"
}

st.set_page_config(page_title="Wie spät ist es?", layout="centered")
st.title("🕒 Wie spät ist es?")

# Selector de ciudad
timezone_name = st.selectbox("🌍 Selecciona una ciudad:", options=list(city_timezones.keys()), format_func=lambda tz: city_timezones[tz])

# Selector de estilo de hora
hour_style = st.radio("🕘 Estilo de hora:", ["Hora digital", "Hora cotidiana (alemán informal)"])

# Hora actual en la zona seleccionada
tz = pytz.timezone(timezone_name)
now = datetime.now(tz)

if hour_style == "Hora digital":
    st.markdown(f"### 🕗 {now.strftime('%H:%M')} ({city_timezones[timezone_name]})")
    hour, minute = now.hour, now.minute
    clock = ClockPlot(hour, minute)
    fig = clock.draw_clock()
    st.pyplot(fig)
else:
    option = st.selectbox("⏱️ Wähle eine Uhrzeit auf Deutsch:", list(examples.keys()))
    hour, minute = examples[option]
    clock = ClockPlot(hour, minute)
    fig = clock.draw_clock()
    st.pyplot(fig)
    st.markdown(f"### Es ist **{option}**")

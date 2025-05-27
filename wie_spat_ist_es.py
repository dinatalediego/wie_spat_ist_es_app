import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pytz
import random

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

partes_dia = [
    (0, 4, "in der Nacht"),
    (5, 9, "am Morgen"),
    (10, 11, "am Vormittag"),
    (12, 13, "am Mittag"),
    (14, 17, "am Nachmittag"),
    (18, 21, "am Abend"),
    (22, 23, "in der Nacht")
]

acciones = [
    "arbeitet", "lernt", "geht spazieren", "kauft ein", "kocht", "liest", "schreibt", "schläft", "hört Musik", "macht Sport"
]

namen = ["Diego", "Julia", "Max", "Anna", "Peter", "Laura", "Tobias", "Nina", "Lukas", "Sophie"]

def get_formal_german(hour, minute):
    return f"Es ist {hour:02d} Uhr {minute:02d}"

def get_part_of_day(hour):
    for start, end, label in partes_dia:
        if start <= hour <= end:
            return label
    return "zu einer unbekannten Zeit"

def generar_oraciones_contextuales(hour):
    tag = get_part_of_day(hour)
    return [f"{random.choice(namen)} {random.choice(acciones)} {tag}." for _ in range(3)]

st.set_page_config(page_title="Wie spät ist es?", layout="centered")
st.title("🕒 Wie spät ist es?")

timezone_name = st.selectbox("🌍 Selecciona una ciudad:", options=list(city_timezones.keys()), format_func=lambda tz: city_timezones[tz])
hour_style = st.radio("🕘 Estilo de hora:", ["Hora digital", "Hora cotidiana (alemán informal)"])

tz = pytz.timezone(timezone_name)
now = datetime.now(tz)

if hour_style == "Hora digital":
    st.markdown(f"### 🕗 {now.strftime('%H:%M')} ({city_timezones[timezone_name]})")
    hour, minute = now.hour, now.minute
    clock = ClockPlot(hour, minute)
    fig = clock.draw_clock()
    st.pyplot(fig)

    st.info(f"**Formal:** {get_formal_german(hour, minute)}")
    st.info(f"**Teil des Tages:** {get_part_of_day(hour)}")
    st.success("**Beispielaktivitäten:**")
    for act in generar_oraciones_contextuales(hour):
        st.markdown(f"- {act}")

else:
    option = st.selectbox("⏱️ Wähle eine Uhrzeit auf Deutsch:", list(examples.keys()))
    hour, minute = examples[option]
    clock = ClockPlot(hour, minute)
    fig = clock.draw_clock()
    st.pyplot(fig)

    st.markdown(f"### Es ist **{option}**")
    st.info(f"**Formal:** {get_formal_german(hour, minute)}")
    st.info(f"**Teil des Tages:** {get_part_of_day(hour)}")
    st.success("**Beispielaktivitäten:**")
    for act in generar_oraciones_contextuales(hour):
        st.markdown(f"- {act}")
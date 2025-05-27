import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pytz
import random
import urllib.parse
import openai

# Obtener la clave API desde los secretos
openai.api_key = st.secrets["openai_api_key"]

# Clase para dibujar el reloj analógico
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

# Clase para explicar gramática relacionada con la hora
class ClockGrammarModule:
    def __init__(self, hour):
        self.hour = hour
        self.part_of_day = self.get_part_of_day()

    def get_part_of_day(self):
        for start, end, label in partes_dia:
            if start <= self.hour <= end:
                return label
        return "zu einer unbekannten Zeit"

    def explain_am_um(self):
        if self.part_of_day.startswith("am"):
            return "👉 Usamos 'am' con partes del día como 'Morgen', 'Abend', 'Nachmittag'."
        elif self.part_of_day == "in der Nacht":
            return "👉 Usamos 'in der Nacht' para referirnos a horas entre 22:00 y 04:00."
        else:
            return "👉 Usamos 'um' con horas exactas, por ejemplo: 'um acht Uhr'."

    def formal_phrase(self, minute):
        return f"Es ist {self.hour:02d} Uhr {minute:02d}"

    def example_activities(self):
        return [f"{random.choice(namen)} {random.choice(acciones)} {self.part_of_day}." for _ in range(3)]

# Función para generar imagen desde DALL·E
def generar_imagen_dalle(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    return response['data'][0]['url']

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

    grammar = ClockGrammarModule(hour)
    st.info(f"**Formal:** {grammar.formal_phrase(minute)}")
    st.info(f"**Teil des Tages:** {grammar.part_of_day}")
    st.warning(grammar.explain_am_um())
    st.success("**Beispielaktivitäten:**")
    frases = grammar.example_activities()
    for act in frases:
        st.markdown(f"- {act}")
        url = f"https://translate.google.com/?sl=de&tl=es&text={urllib.parse.quote(act)}"
        st.markdown(f"[🔗 Traducir con Google Translate]({url})")
        if st.button(f"🎨 Generar imagen de: '{act}'", key=act):
            image_url = generar_imagen_dalle(act)
            st.image(image_url, caption=act)

else:
    option = st.selectbox("⏱️ Wähle eine Uhrzeit auf Deutsch:", list(examples.keys()))
    hour, minute = examples[option]
    clock = ClockPlot(hour, minute)
    fig = clock.draw_clock()
    st.pyplot(fig)

    st.markdown(f"### Es ist **{option}**")
    grammar = ClockGrammarModule(hour)
    st.info(f"**Formal:** {grammar.formal_phrase(minute)}")
    st.info(f"**Teil des Tages:** {grammar.part_of_day}")
    st.warning(grammar.explain_am_um())
    st.success("**Beispielaktivitäten:**")
    frases = grammar.example_activities()
    for act in frases:
        st.markdown(f"- {act}")
        url = f"https://translate.google.com/?sl=de&tl=es&text={urllib.parse.quote(act)}"
        st.markdown(f"[🔗 Traducir con Google Translate]({url})")
        if st.button(f"🎨 Generar imagen de: '{act}'", key=act):
            image_url = generar_imagen_dalle(act)
            st.image(image_url, caption=act)

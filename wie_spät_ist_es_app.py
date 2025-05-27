import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pytz
import random
import urllib.parse
import openai

# Configuración inicial de la app
st.set_page_config(page_title="🕒 Wie spät ist es?", layout="centered")

# Estilos personalizados
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
        font-family: "Segoe UI", sans-serif;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #f0f0f0;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
        color: #1f4e79;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# API Key de OpenAI
openai.api_key = st.secrets["openai_api_key"]

# Datos
acciones = [
    "arbeitet", "lernt", "geht spazieren", "kauft ein", "kocht", "liest", 
    "schreibt", "schläft", "hört Musik", "macht Sport"
]
namen = ["Diego", "Julia", "Max", "Anna", "Peter", "Laura", "Tobias", "Nina", "Jean", "Sophie"]
partes_dia = [
    (0, 4, "in der Nacht"), (5, 9, "am Morgen"), (10, 11, "am Vormittag"),
    (12, 13, "am Mittag"), (14, 17, "am Nachmittag"), (18, 21, "am Abend"),
    (22, 23, "in der Nacht")
]
examples = {
    "fünf nach elf": (11, 5), "zehn nach drei": (3, 10), "Viertel nach zehn": (10, 15),
    "20 nach sechs": (6, 20), "fünf vor halb acht": (7, 25), "halb zwei": (1, 30),
    "fünf nach halb eins": (12, 35), "halb drei": (2, 30), "fünf vor drei": (2, 55)
}
city_timezones = {
    "Europe/Berlin": "🇩🇪 Berlin", "America/Lima": "🇵🇪 Lima", "Europe/London": "🇬🇧 London",
    "America/New_York": "🇺🇸 New York", "Asia/Tokyo": "🇯🇵 Tokyo", 
    "Australia/Sydney": "🇦🇺 Sydney", "Asia/Dubai": "🇦🇪 Dubai", 
    "Africa/Johannesburg": "🇿🇦 Johannesburg", "America/Mexico_City": "🇲🇽 Ciudad de México"
}

# Clases
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

def generar_imagen_dalle(prompt):
    response = openai.Image.create(prompt=prompt, n=1, size="256x256")
    return response['data'][0]['url']

# UI Principal
st.title("🕒 Wie spät ist es?")
tabs = st.tabs(["🕘 Hora actual", "🕰️ Ejemplos en alemán"])

# === TAB 1: HORA ACTUAL ===
with tabs[0]:
    timezone_name = st.selectbox("🌍 Selecciona una ciudad:", options=list(city_timezones.keys()),
                                 format_func=lambda tz: city_timezones[tz])
    tz = pytz.timezone(timezone_name)
    now = datetime.now(tz)
    hour, minute = now.hour, now.minute

    st.markdown(f"## 🕗 {now.strftime('%H:%M')} ({city_timezones[timezone_name]})")

    reloj = ClockPlot(hour, minute)
    st.pyplot(reloj.draw_clock())

    gram = ClockGrammarModule(hour)
    st.info(f"**Formal:** {gram.formal_phrase(minute)}")
    st.success(f"**Parte del día:** {gram.part_of_day}")
    st.warning(gram.explain_am_um())

    st.markdown("### 📚 Ejemplos de actividades:")
    for frase in gram.example_activities():
        st.markdown(f"- {frase}")
        st.markdown(f"[🔗 Traducir en Google Translate](https://translate.google.com/?sl=de&tl=es&text={urllib.parse.quote(frase)})")
        if st.button(f"🎨 Imagen de: '{frase}'", key=frase):
            st.image(generar_imagen_dalle(frase), caption=frase)

# === TAB 2: HORA DE EJEMPLO ===
with tabs[1]:
    option = st.selectbox("🕯️ Elige una hora en alemán:", list(examples.keys()))
    hour, minute = examples[option]
    st.markdown(f"## Es ist **{option}**")

    reloj = ClockPlot(hour, minute)
    st.pyplot(reloj.draw_clock())

    gram = ClockGrammarModule(hour)
    st.info(f"**Formal:** {gram.formal_phrase(minute)}")
    st.success(f"**Parte del día:** {gram.part_of_day}")
    st.warning(gram.explain_am_um())

    st.markdown("### 📚 Ejemplos de actividades:")
    for frase in gram.example_activities():
        st.markdown(f"- {frase}")
        st.markdown(f"[🔗 Traducir en Google Translate](https://translate.google.com/?sl=de&tl=es&text={urllib.parse.quote(frase)})")
        if st.button(f"🎨 Imagen de: '{frase}'", key=frase):
            st.image(generar_imagen_dalle(frase), caption=frase)

# Footer de contacto
st.markdown("---")
st.markdown("📬 ¿Sugerencias o dudas? [Contáctanos](mailto:soporte@app.com)")

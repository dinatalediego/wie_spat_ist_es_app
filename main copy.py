import streamlit as st
from datetime import datetime
from utils.reloj import ClockPlot, ClockGrammarModule, generar_imagen_dalle
import pytz
import urllib.parse
from utils.progreso import init_session_state, registrar_frase, mostrar_progreso

# CONFIGURACIÓN
st.set_page_config(page_title="🕒 Wie spät ist es?", layout="wide")

# ESTILOS PERSONALIZADOS (opcional si usas /assets/custom.css)
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        border-radius: 10px;
        padding: 0.4em 1em;
        font-weight: bold;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ZONAS HORARIAS
city_timezones = {
    "Europe/Berlin": "🇩🇪 Berlín",
    "America/Lima": "🇵🇪 Lima",
    "Europe/London": "🇬🇧 Londres",
    "America/New_York": "🇺🇸 Nueva York",
    "Asia/Tokyo": "🇯🇵 Tokio",
    "Australia/Sydney": "🇦🇺 Sídney",
    "Asia/Dubai": "🇦🇪 Dubái",
    "Africa/Johannesburg": "🇿🇦 Johannesburgo",
    "America/Mexico_City": "🇲🇽 Ciudad de México"
}

# FRASES MODELO
examples = {
    "fünf nach elf": (11, 5), "zehn nach drei": (3, 10), "Viertel nach zehn": (10, 15),
    "20 nach sechs": (6, 20), "fünf vor halb acht": (7, 25), "halb zwei": (1, 30),
    "fünf nach halb eins": (12, 35), "halb drei": (2, 30), "fünf vor drei": (2, 55)
}

# TABS DE LA APP
st.title("🕒 Wie spät ist es? | Aprende alemán con horas reales")
tab1, tab2 = st.tabs(["📍 Hora actual", "🧠 Ejemplos educativos"])

# TAB 1: Hora actual en ciudad
with tab1:
    zona = st.selectbox("🌍 Selecciona una ciudad:", list(city_timezones.keys()),
                        format_func=lambda x: city_timezones[x])
    now = datetime.now(pytz.timezone(zona))
    hora, minuto = now.hour, now.minute

    st.markdown(f"### 🕘 Hora actual en {city_timezones[zona]}: **{now.strftime('%H:%M')}**")

    reloj = ClockPlot(hora, minuto)
    st.pyplot(reloj.draw_clock())

    gram = ClockGrammarModule(hora)
    st.info(f"🧾 **Formal:** {gram.formal_phrase_con_letras(minuto)}")
    st.success(f"📍 Parte del día: {gram.part_of_day}")
    st.warning(gram.explain_am_um())

    st.markdown("### 📚 Frases cotidianas:")
    for frase in gram.example_activities_con_hora(minuto):
        st.markdown(f"- {frase}")
        st.markdown(f"[🔗 Traducir](https://translate.google.com/?sl=de&tl=es&text={urllib.parse.quote(frase)})")
        if st.button(f"🎨 Imagen de: {frase}", key=frase):
            st.image(generar_imagen_dalle(frase), caption=frase)

# TAB 2: Hora ejemplo en alemán
with tab2:
    ejemplo = st.selectbox("🕰️ Elige una hora en alemán:", list(examples.keys()))
    h, m = examples[ejemplo]

    st.markdown(f"### 🕒 Es ist **{ejemplo}**")

    reloj = ClockPlot(h, m)
    st.pyplot(reloj.draw_clock())

    gram = ClockGrammarModule(h)
    st.info(f"🧾 **Formal:** {gram.formal_phrase_con_letras(m)}")
    st.success(f"📍 Parte del día: {gram.part_of_day}")
    st.warning(gram.explain_am_um())

    st.markdown("### 📚 Frases cotidianas:")
    for frase in gram.example_activities_con_hora(m):
        st.markdown(f"- {frase}")
        st.markdown(f"[🔗 Traducir](https://translate.google.com/?sl=de&tl=es&text={urllib.parse.quote(frase)})")
        if st.button(f"🎨 Imagen de: {frase}", key=frase):
            st.image(generar_imagen_dalle(frase), caption=frase)

st.markdown("---")
st.markdown("📬 ¿Sugerencias? [Contáctanos](mailto:hallo@sprachtime.ai)")

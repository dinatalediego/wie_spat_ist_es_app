import streamlit as st

# Inicializar frases vistas
def init_session_state():
    if "frases_vistas" not in st.session_state:
        st.session_state.frases_vistas = set()

# Registrar frase como aprendida
def registrar_frase(frase):
    st.session_state.frases_vistas.add(frase)

# Obtener nivel actual
def obtener_nivel():
    total = len(st.session_state.frases_vistas)
    if total < 5:
        return "🥉 Principiante"
    elif total < 10:
        return "🥈 Intermedio"
    else:
        return "🥇 Avanzado"

# Mostrar progreso visual
def mostrar_progreso(total_frases):
    vistas = len(st.session_state.frases_vistas)
    progreso = vistas / total_frases
    st.markdown(f"**Progreso:** {vistas}/{total_frases} frases vistas")
    st.progress(progreso)
    st.markdown(f"**Nivel actual:** {obtener_nivel()}")

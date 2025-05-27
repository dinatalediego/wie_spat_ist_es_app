import matplotlib.pyplot as plt
import numpy as np
import openai
import random

# Configurar clave API
openai.api_key = open(".streamlit/secrets.toml").read().split('=')[1].strip().replace('"', '')

# Diccionario para conversión de números al alemán
unidades = ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun"]
especiales = {
    10: "zehn", 11: "elf", 12: "zwölf", 13: "dreizehn", 14: "vierzehn",
    15: "fünfzehn", 16: "sechzehn", 17: "siebzehn", 18: "achtzehn", 19: "neunzehn"
}
decenas = {
    20: "zwanzig", 30: "dreißig", 40: "vierzig", 50: "fünfzig"
}

def numero_en_aleman(n):
    if n < 10:
        return unidades[n]
    elif 10 <= n < 20:
        return especiales[n]
    else:
        u = n % 10
        d = n - u
        if u == 0:
            return decenas[d]
        else:
            return f"{unidades[u]}und{decenas[d]}"

# Gramática del día
acciones = ["arbeitet", "lernt", "geht spazieren", "kauft ein", "kocht", "liest",
            "schreibt", "schläft", "hört Musik", "macht Sport"]
namen = ["Diego", "Julia", "Max", "Anna", "Peter", "Laura", "Tobias", "Nina", "Jean", "Sophie"]
partes_dia = [
    (0, 4, "in der Nacht"), (5, 9, "am Morgen"), (10, 11, "am Vormittag"),
    (12, 13, "am Mittag"), (14, 17, "am Nachmittag"), (18, 21, "am Abend"), (22, 23, "in der Nacht")
]

# Clase para el reloj visual
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
            ax.text(np.cos(angle)*0.85, np.sin(angle)*0.85, str(i), ha='center', va='center', fontsize=10)

        angle_min = np.pi/2 - 2*np.pi * (self.minute / 60)
        ax.plot([0, np.cos(angle_min)*0.9], [0, np.sin(angle_min)*0.9], lw=2, color='blue')

        angle_hour = np.pi/2 - 2*np.pi * ((self.hour + self.minute/60) / 12)
        ax.plot([0, np.cos(angle_hour)*0.6], [0, np.sin(angle_hour)*0.6], lw=3, color='black')

        return fig

# Clase de gramática y ejemplos
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
            return "👉 Usamos 'in der Nacht' entre 22:00 y 04:00."
        else:
            return "👉 Usamos 'um' con horas exactas, por ejemplo: 'um acht Uhr'."

    def formal_phrase(self, minute):
        return f"Es ist {self.hour:02d} Uhr {minute:02d}"

    def formal_phrase_con_letras(self, minute):
        hora_letras = numero_en_aleman(self.hour)
        minuto_letras = numero_en_aleman(minute)
        return f"Es ist {hora_letras} Uhr {minuto_letras}"

    def example_activities_con_hora(self, minute):
        tiempo = f"um {self.hour:02d}:{minute:02d} Uhr"
        return [f"{random.choice(namen)} {random.choice(acciones)} {tiempo} {self.part_of_day}." for _ in range(3)]

# Función DALL·E
def generar_imagen_dalle(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    return response['data'][0]['url']

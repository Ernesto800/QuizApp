import time as tm
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import random
import json
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PREGUNTAS_PATH = os.path.join(BASE_DIR, 'preguntasGenerales.json')
RANKING_PATH = os.path.join(BASE_DIR, 'ranking.json')




ventana = tk.Tk()
ventana.title("QUIZ APP")
ventana.attributes('-fullscreen', True)
ventana.config(bg="lightblue")

def actualizar_fuentes(event):
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    tamano_fuente = min(ancho, alto) // 30  # Ajusta el divisor según tus necesidades
    fuente = tkFont.Font(family="Helvetica", size=tamano_fuente)

    for widget in ventana.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
            widget.config(font=fuente)

ventana.bind('<Configure>', actualizar_fuentes)

def iniciar_quiz():
    nombreParticipante = entrada_nombre.get()
    print(f"¡Hola, {nombreParticipante}! Espero que disfrutes el quiz.")
    mostrar_opciones(nombreParticipante)
    
def guardar_ranking(nombre, puntaje):
    """Guarda el nombre y puntaje en el archivo ranking.json"""
    ranking = []

    try:
        with open(RANKING_PATH, 'r', encoding='utf-8') as archivo:
            ranking = json.load(archivo)
    except FileNotFoundError:
        pass

    ranking.append({'nombre': nombre, 'puntaje': puntaje})

    with open(RANKING_PATH, 'w', encoding='utf-8') as archivo:
        json.dump(ranking, archivo, indent=4)

def mostrarRanking(nombre):
    for widget in ventana.winfo_children():
            widget.destroy()

    try:
        with open('ranking.json', 'r',encoding='utf-8') as archivo:
            ranking = json.load(archivo)
            etiqueta1 = tk.Label(ventana, text="\nRanking de Participantes:", bg='lightblue')
            etiqueta1.pack(pady=20,expand=True, fill='both')
            for participante in ranking:
                etiqueta2 = tk.Label(ventana,text=f"Nombre: {participante['nombre']}, Puntaje: {participante['puntaje']}", bg='lightblue')
                etiqueta2.pack(pady=10,expand=True, fill='both')
    except FileNotFoundError:
        etiqueta3 = tk.Label(ventana, text="No hay datos de ranking disponibles.")
        etiqueta3.pack(pady=20,expand=True, fill='both')

    boton_volver = tk.Button(ventana, text="Volver", command=lambda: mostrar_opciones(nombre))
    boton_volver.pack(pady=20)


class PreguntasQuiz:
    def __init__(self):
        self.contador = 0
        self.pregunta_actual = 0
        self.preguntas = []

    def mostrar_cuentatras(self,nombre):
        for widget in ventana.winfo_children():
            widget.destroy()


        frame_opciones = tk.Frame(ventana, bg='lightblue')
        frame_opciones.pack(expand=True)

        fuente_grande = tkFont.Font(family="Helvetica", size=40)

        etiquetanombre = tk.Label(frame_opciones, text=f"¡Hola, {nombre}! Espero que disfrutes el quiz.", font=fuente_grande, anchor='center',bg='lightblue')
        etiqueta1 = tk.Label(frame_opciones, text="El Quiz está a punto de comenzar.", font=fuente_grande, anchor='center',bg='lightblue')
        etiqueta2 = tk.Label(frame_opciones, text="Hay un total de 10 preguntas. ¡Suerte!", font=fuente_grande, anchor='center',bg='lightblue')
        etiquetanombre.pack(pady=20,expand=True, fill='both')
        etiqueta1.pack(pady=20,expand=True, fill='both')
        etiqueta2.pack(pady=20,expand=True, fill='both')

        etiqueta3 = tk.Label(frame_opciones, text="", font=fuente_grande, anchor='center', bg='lightblue')
        etiqueta3.pack(pady=10,expand=True, fill='both')

        for segundos in range(5, 0, -1):
            etiqueta3.config(text=f"Comienza en {segundos}...", font=fuente_grande, anchor='center', bg='lightblue')
            ventana.update()
            tm.sleep(1)

        etiqueta3.config(text="¡Comenzamos!\n")
        ventana.update()
        tm.sleep(1)
        self.mostrar_pregunta(nombre)

    def manejar_respuesta(self, respuesta, opcionCorrecta, nombre):
        seleccion = respuesta
        if respuesta == opcionCorrecta:
            resultado = f"\nTu respuesta ha sido: {seleccion}\n¡Correcta!"
            self.contador += 1
        else:
            resultado = f"\nTu respuesta ha sido: {seleccion}\nIncorrecta"

        for widget in ventana.winfo_children():
            widget.destroy()

        etiqueta_resultado = tk.Label(ventana, text=resultado, wraplength=800, bg='lightblue')
        etiqueta_resultado.pack(pady=20,expand=True, fill='both')

        boton_siguiente = tk.Button(ventana, text="Siguiente", command=lambda: self.siguiente_pregunta(nombre))
        boton_siguiente.pack(pady=20)

    def siguiente_pregunta(self, nombre):
        self.pregunta_actual += 1
        if self.pregunta_actual < len(self.preguntas):
            self.mostrar_pregunta(nombre)
        else:
            self.mostrar_resultado_final(nombre)

    def mostrar_resultado_final(self, nombre):
        for widget in ventana.winfo_children():
            widget.destroy()
        resultado_final = f"Has acertado {self.contador} preguntas!"
        etiqueta_final = tk.Label(ventana, text=resultado_final, bg='lightblue')
        etiqueta_final.pack(pady=20,expand=True, fill='both')
        guardar_ranking(nombre, self.contador)
        boton_volver = tk.Button(ventana, text="Volver al inicio", command=lambda: mostrar_opciones(nombre))
        boton_volver.pack(pady=20)

    def mostrar_pregunta(self, nombre):
        for widget in ventana.winfo_children():
            widget.destroy()

        if self.pregunta_actual < len(self.preguntas):
            pregunta = self.preguntas[self.pregunta_actual]
            texto_pregunta, resp1, resp2, resp3, resp4, opcionCorrecta = pregunta

            etiqueta_pregunta = tk.Label(ventana, text=texto_pregunta, bg='lightblue')
            etiqueta_pregunta.pack(pady=20,expand=True, fill='both')

            respuesta_1 = tk.Button(ventana, text=resp1, command=lambda: self.manejar_respuesta(resp1, opcionCorrecta, nombre), bg='red')
            respuesta_2 = tk.Button(ventana, text=resp2, command=lambda: self.manejar_respuesta(resp2, opcionCorrecta, nombre), bg='green')
            respuesta_3 = tk.Button(ventana, text=resp3, command=lambda: self.manejar_respuesta(resp3, opcionCorrecta, nombre), bg='blue')
            respuesta_4 = tk.Button(ventana, text=resp4, command=lambda: self.manejar_respuesta(resp4, opcionCorrecta, nombre), bg='yellow')

            respuesta_1.pack(pady=5,expand=True, fill='both')
            respuesta_2.pack(pady=5,expand=True, fill='both')
            respuesta_3.pack(pady=5,expand=True, fill='both')
            respuesta_4.pack(pady=5,expand=True, fill='both')
        else:
            self.mostrar_resultado_final(nombre)


def PreguntasGenerales():
    with open(PREGUNTAS_PATH, 'r', encoding='utf-8') as archivo:
        ListQuestion = json.load(archivo)
    
    ListQuestion = [tuple(pregunta) for pregunta in ListQuestion if isinstance(pregunta, list)]
    random.shuffle(ListQuestion)
    return ListQuestion


def ComenzarJuego(nombre):
    quiz = PreguntasQuiz()
    quiz.preguntas = PreguntasGenerales()
    quiz.mostrar_cuentatras(nombre)


def mostrar_opciones(nombre):
    for widget in ventana.winfo_children():
        widget.destroy()

    frame_opciones = tk.Frame(ventana, bg='lightblue')
    frame_opciones.pack(expand=True)

    fuente_grande = tkFont.Font(family="Helvetica", size=40)

   
    boton_comenzar_juego = tk.Button(frame_opciones, text="Comenzar a jugar", font=fuente_grande, command=lambda: ComenzarJuego(nombre), anchor='center')
    boton_consultar_ranking = tk.Button(frame_opciones, text="Consultar el Ranking", font=fuente_grande, command=lambda: mostrarRanking(nombre), anchor='center')
    boton_salir = tk.Button(frame_opciones, text="Salir", font=fuente_grande, command=ventana.quit, anchor='center')
    boton_comenzar_juego.pack(pady=10)
    boton_consultar_ranking.pack(pady=10)
    boton_salir.pack(pady=10)


frame_centrada = tk.Frame(ventana, bg='lightblue')
frame_centrada.pack(expand=True)

fuente_grande = tkFont.Font(family="Helvetica", size=40)


etiqueta = tk.Label(frame_centrada, text="Ingresa tu nombre:", font=fuente_grande, anchor='center', bg='lightblue')
etiqueta.pack(pady=20, fill='x')

entrada_nombre = tk.Entry(frame_centrada, font=fuente_grande, width=30, bg='black', fg='white')
entrada_nombre.pack(pady=10, fill='x')


boton_comenzar = tk.Button(frame_centrada, text="Comenzar Quiz", font=fuente_grande, command=iniciar_quiz)
boton_comenzar.pack(pady=20, fill='x')


ventana.mainloop()

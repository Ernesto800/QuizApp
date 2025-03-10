import time as tm
import random
import json

def mostrar_bienvenida():
    print("Bienvenido a el Quiz App contrarreloj!!")
    nombreParticipante = input("Introduce tu nombre:")
    print(f"¡Hola, {nombreParticipante}! Espero que disfrutes el quiz.")
    return nombreParticipante

def guardar_ranking(nombre, puntaje):
    """Guarda el nombre y puntaje en el archivo ranking.json"""
    ranking = []


    try:
        with open('ranking.json', 'r') as archivo:
            ranking = json.load(archivo)
    except FileNotFoundError:
        pass

    ranking.append({'nombre': nombre, 'puntaje': puntaje})

    with open('ranking.json', 'w') as archivo:
        json.dump(ranking, archivo, indent=4)

def mostrar_ranking():
    """Muestra el ranking almacenado en ranking.json"""
    try:
        with open('ranking.json', 'r') as archivo:
            ranking = json.load(archivo)
            print("\nRanking de Participantes:")
            for participante in ranking:
                print(f"Nombre: {participante['nombre']}, Puntaje: {participante['puntaje']}")
    except FileNotFoundError:
        print("No hay datos de ranking disponibles.")



class PreguntasQuiz:
    def __init__(self):
        self.contador = 0

    def cuenta_regresiva_inicio(self):
        """Cuenta regresiva antes de empezar el quiz."""
        print("El Quiz está a punto de comenzar.")
        print("Tienes 30 segundos para responder cada pregunta.")
        print("Hay un total de preguntas. ¡Suerte!")
        for segundos in range(5, 0, -1):
            print(f"\rComienza en {segundos}...", end="", flush=True)
            tm.sleep(1)
        print("\n¡Comenzamos!\n")

    def manejar_respuesta(self, resp1, resp2, resp3, resp4, opcionCorrecta):
        """Este método maneja la lógica de validación de la respuesta."""
        while True:
            respuesta = input("\nEscribe tu respuesta aquí: ")
            seleccion = resp1 if respuesta == "1" else resp2 if respuesta == "2" else resp3 if respuesta == "3" else resp4
            if respuesta == opcionCorrecta:
                print(f"\nTu respuesta ha sido: {seleccion}")
                print("¡Correcta!")
                self.contador += 1
                print(f"Has acertado {self.contador} preguntas!")
                break
            elif respuesta in ["1", "2", "3", "4"]:
                seleccion = resp1 if respuesta == "1" else resp2 if respuesta == "2" else resp3 if respuesta == "3" else resp4
                print(f"\nTu respuesta ha sido: {seleccion}")
                print("Incorrecta")
                break
            else:
                print("\nRespuesta no válida. Por favor, elige 1, 2 o 3.")

    def hacer_pregunta(self, numero_pregunta,texto_pregunta, resp1, resp2, resp3, resp4, opcionCorrecta):
        """Muestra la pregunta y llama a manejar_respuesta."""
        print(f"\nPregunta {numero_pregunta}: {texto_pregunta}")
        print(f"Tus opciones son:")
        print(f"1. {resp1}")
        print(f"2. {resp2}")
        print(f"3. {resp3}")
        print(f"4. {resp4}")
        print("Introduce 1, 2, 3 o 4 como respuesta")
        
        self.manejar_respuesta(resp1, resp2, resp3, resp4, opcionCorrecta)

def PreguntasGenerales():
    with open('preguntasGenerales.json', 'r', encoding='utf-8') as archivo:
        ListQuestion = json.load(archivo)
    
    ListQuestion = [tuple(pregunta) for pregunta in ListQuestion if isinstance(pregunta, list)]
    random.shuffle(ListQuestion)
    return ListQuestion

nombre = mostrar_bienvenida()
while True:
    print()

    print("1. Comenzar a jugar")
    print("2. Consultar el Ranking")
    print("3. Salir")

    option = input("Selecciona una acción:")

    match option:
        case "1":          
            quiz = PreguntasQuiz()
            quiz.cuenta_regresiva_inicio()
            preguntasGeneral = PreguntasGenerales()
            numero_pregunta = 1 
            for pregunta in preguntasGeneral:
                if pregunta is not None and isinstance(pregunta, tuple):
                    quiz.hacer_pregunta(numero_pregunta, *pregunta)
                    numero_pregunta += 1
                else:
                    print("¡Pregunta inválida detectada!")

            print("")
            print(f"HAS ACERTADO UN TOTAL DE: {quiz.contador} PREGUNTAS!!!")
            guardar_ranking(nombre, quiz.contador)
            while True:
                option = input("Introduce 1 para volver a el inicio: ")
                if option == "1":
                    break

        case "2":
            mostrar_ranking()
            pass
        case "3":
            print("Saliendo del Quiz...")
            break
        case _:
            print("Opción inválida. Por favor, selecciona una nueva")
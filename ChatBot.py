import os
from dotenv import load_dotenv
import mariadb
from colorama import init, Fore, Back, Style

load_dotenv()

# Conexión a la base de datos MariaDB
conexion = mariadb.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USER'),
    password=os.getenv('PASS'),
    database=os.getenv('DATABASE')
)
cursor = conexion.cursor()

#Buscamos si existe una respuesta al mensaje del usuario en la base de datos
def obtener_respuesta(mensaje):
    # Convertir el mensaje a minúsculas antes de buscar en la base de datos
    mensaje = mensaje.lower()
    consulta = "SELECT Respuesta FROM chat WHERE Mensaje = ?"
    cursor.execute(consulta, (mensaje,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

# Observamos si el usuario se está  despidiendo para terminar la sesión
def Despedida(mensaje):
    mensaje = mensaje.lower()
    consulta = "SELECT Despedida FROM despedida WHERE Despedida = ?"
    cursor.execute(consulta, (mensaje,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def guardar_respuesta(mensaje, respuesta):
    # Convertir tanto el mensaje como la respuesta a minúsculas antes de guardarlos
    mensaje = mensaje.lower()
    respuesta = respuesta.lower()
    consulta = "INSERT INTO chat (Mensaje, Respuesta) VALUES (?, ?)"
    cursor.execute(consulta, (mensaje, respuesta))
    conexion.commit()

print(Fore.RED+"¡Hola! Soy un chatbot. Escribe 'salir' para terminar la conversación.")

while True:
    mensaje_usuario = input(Fore.BLUE +"Tú: ")
    despedida = Despedida(mensaje_usuario)
    if despedida :
        print(Fore.RED+"¡Adiós!")
        print(Fore.WHITE+"")
        break

    respuesta = obtener_respuesta(mensaje_usuario)
    
    if respuesta:
        print(Fore.RED+f"Chatbot: {respuesta}")
    else:
        print(Fore.RED+"Chatbot: No sé cómo responder a eso. ¿Qué debería decir?")
        nueva_respuesta = input(Fore.BLUE+"Tú: ")
        guardar_respuesta(mensaje_usuario, nueva_respuesta)
        print(Fore.RED+"Chatbot: ¡Gracias! Ahora lo recordaré para la próxima vez.")
        print(Fore.WHITE+"")

# Cerrar conexión
cursor.close()
# Cerramos la sesión de la base de datos
conexion.close()

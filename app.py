
import threading
from auth import Auth
from services.group_service import get_groups
from services.room_service import get_rooms
from services.company_service import get_companies
from services.category_service import get_categories 
from services.style_service import get_styles, get_style_info, create_style

import sys
	# Variables globales
auth_instance = None
session_timeout = 300 # Tiempo de espera en segundos (5 minutos)
timer = None

def solicitar_credenciales():
    global auth_instance
    email = input("Introduce tu correo electrónico: ")
    password = input("Introduce tu contraseña: ")
    auth_instance = Auth(email, password)
    obtener_token()

def obtener_token():
    try:
        token = auth_instance.get_token()
        reiniciar_temporizador()  # Reinicia el temporizador de inactividad
    except Exception as e:
        print(f"Error al obtener el token: {e}")
        solicitar_credenciales()

def menu():
    print("\n--- Menú de Microservicios ---")
    print("1: Obtener grupos")
    print("2: Obtener rooms")
    print("3: Obtener compañías")
    print("4: Obtener categorías")
    print("5: Obtener estilos")
    print("6: Obtener detalles de un estilo")
    print("7: Crear un nuevo estilo")  # Opción para crear un estilo
    print("8: Cerrar sesión")
    print("9: Salir")

def obtener_grupos():
    try:
        groups = get_groups(auth_instance)
        print("Grupos obtenidos:", groups)
        reiniciar_temporizador()
    except Exception as e:
        print(f"Error al obtener los grupos: {e}")

def obtener_rooms():
    try:
        group_id = input("Introduce el ID del grupo para obtener los rooms: ")
        rooms = get_rooms(auth_instance, group_id)
        print("Rooms obtenidos:", rooms)
        reiniciar_temporizador()
    except Exception as e:
        print(f"Error al obtener los rooms: {e}")

def obtener_companies():
    try:
        group_id = input("Introduce el ID del grupo para obtener las compañías: ")
        companies = get_companies(auth_instance, group_id)
        print("Compañías obtenidas:", companies)
        reiniciar_temporizador()
    except Exception as e:
        print(f"Error al obtener las compañías: {e}")

def obtener_categories():
    try:
        company_id = input("Introduce el ID de la compañía para obtener las categorías: ")
        categories = get_categories(auth_instance, company_id)
        print("Categorías obtenidas:", categories)
        reiniciar_temporizador()
    except Exception as e:
        print(f"Error al obtener las categorías: {e}")

def obtener_styles():
    try:
        group_id = input("Introduce el ID del grupo para obtener los estilos: ")
        styles = get_styles(auth_instance, group_id)
        print("Estilos obtenidos:", styles)
        reiniciar_temporizador()
    except Exception as e:
        print(f"Error al obtener los estilos: {e}")

def obtener_detalle_estilo():
    try:
        style_id = input("Introduce el ID del estilo para obtener su detalle: ")
        style_info = get_style_info(auth_instance, style_id)
        print("Detalles del estilo:", style_info)
        reiniciar_temporizador()
    except Exception as e:
        print(f"Error al obtener el detalle del estilo: {e}")

def crear_nuevo_estilo():
    try:
        room_id = input("Introduce el ID del room: ")
        style_number = input("Introduce el nombre del estilo (styleNumber): ")
        description = input("Introduce la descripción del estilo: ")
        tags = input("Introduce los tags, separados por comas: ")
        
        style = create_style(auth_instance, room_id, style_number, description, tags)
        print("Estilo creado exitosamente:", style)
        reiniciar_temporizador()
    except Exception as e:
        print(f"Error al crear el estilo: {e}")

def iniciar_temporizador():
    global timer
    timer = threading.Timer(session_timeout, expirar_sesion)
    timer.start()

def reiniciar_temporizador():
    global timer
    if timer is not None:
        timer.cancel()
    iniciar_temporizador()

def expirar_sesion():
    print("\n--- Sesión expirada por inactividad ---\n")
    solicitar_credenciales()

# Programa principal
if __name__ == "__main__":
    print("Bienvenido a la aplicación de integración con CLO-SET.")
    solicitar_credenciales()

    while True:
        menu()
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            reiniciar_temporizador()
            obtener_grupos()
        elif opcion == "2":
            reiniciar_temporizador()
            obtener_rooms()
        elif opcion == "3":
            reiniciar_temporizador()
            obtener_companies()
        elif opcion == "4":
            reiniciar_temporizador()
            obtener_categories()
        elif opcion == "5":
            reiniciar_temporizador()
            obtener_styles()
        elif opcion == "6":
            reiniciar_temporizador()
            obtener_detalle_estilo()
        elif opcion == "7":
            reiniciar_temporizador()
            crear_nuevo_estilo()
        elif opcion == "8":
            print("Cerrando sesión...")
            if timer is not None:
                timer.cancel()
            solicitar_credenciales()
        elif opcion == "9":
            print("Saliendo de la aplicación...")
            if timer is not None:
                timer.cancel()
            sys.exit()
 
        else:
            print("Opción no válida. Por favor, selecciona una opción del menú.")
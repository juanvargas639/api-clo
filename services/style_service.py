import requests
import os

def get_styles(auth_instance, group_id):
    """
    Obtiene los estilos para un grupo específico.
    """
    url = f"https://www.clo-set.com/api/styles?groupId={group_id}"
    headers = auth_instance.get_auth_header()
    headers["Content-Type"] = "application/json"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Devuelve la lista de estilos
    else:
        try:
            error_data = response.json()
            code = error_data.get("code", "Sin código")
            message = error_data.get("message", "Sin mensaje")
        except ValueError:
            code = response.status_code
            message = response.text or "Error desconocido"
        raise Exception(f"Error {code} - {message}")

def get_style_info(auth_instance, style_id):
    """
    Obtiene la información detallada de un estilo específico por su ID.
    """
    url = f"https://www.clo-set.com/api/styles/{style_id}/versions/0"
    headers = auth_instance.get_auth_header()
    headers["Content-Type"] = "application/json"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Devuelve los detalles del estilo
    else:
        try:
            error_data = response.json()
            code = error_data.get("code", "Sin código")
            message = error_data.get("message", "Sin mensaje")
        except ValueError:
            code = response.status_code
            message = response.text or "Error desconocido"
        raise Exception(f"Error {code} - {message}")
    
import requests
import os

def create_style(auth_instance, room_id, style_number, description, tags):
    """
    Crea un nuevo estilo en CLO-SET.
    """
    url = "https://www.clo-set.com/api/styles"
    headers = auth_instance.get_auth_header()  # Autenticación necesaria
    headers.pop("Content-Type", None)

    # Ruta al archivo de la tela
    file_path = os.path.join("telas", "tela1.zfab")
    
    # Verificar si el archivo existe
    if not os.path.isfile(file_path):
        raise Exception(f"Archivo no encontrado: {file_path}")

    # Configuración para multipart/form-data
    files = {
        "file": ("tela1.zfab", open(file_path, "rb"), "application/octet-stream")
    }
    data = {
        "roomId": room_id,
        "styleNumber": style_number,
        "fileType": 0,  # Definido como 0 para este tipo de estilo
        "description": description,
        "tags": tags  # Enviado como texto, puede ser una lista separada por comas
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    # Manejo de la respuesta y cierre del archivo
    files["file"][1].close()  # Cierra el archivo después de la solicitud

    if response.status_code == 201:
        return response.text.strip()  # Devuelve el ID del estilo como texto plano
    else:
        try:
            error_data = response.json()
            code = error_data.get("code", "Sin código")
            message = error_data.get("message", "Sin mensaje")
        except ValueError:
            code = response.status_code
            message = response.text or "Error desconocido"
        raise Exception(f"Error {code} - {message}")

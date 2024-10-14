import requests

def get_groups(auth_instance):

    url = "https://www.clo-set.com/api/groups"

    headers = auth_instance.get_auth_header()
    headers["Content-Type"] = "application/json"
    # Parámetros opcionales para filtrar por spaceType y spaceId
    params = {
    }

    try:
        response = requests.get(url, headers=headers)
        
        # Verifica si el contenido de la respuesta existe y es JSON
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                # Error si el contenido no se puede decodificar como JSON
                raise Exception("Error en el formato de respuesta, no es JSON válido.")
        else:
            # Intento de decodificar el mensaje de error si está en JSON
            try:
                error_data = response.json()
                code = error_data.get("code", "Sin código")
                message = error_data.get("message", "Sin mensaje")
            except ValueError:
                # Si no hay contenido en JSON, maneja como texto plano
                code = response.status_code
                message = response.text if response.text else "Sin respuesta del servidor"
                
            raise Exception(f"Error {code} - {message}")
    
    except requests.RequestException as e:
        # Error de conexión o de tiempo de espera
        raise Exception(f"Error de conexión: {e}")

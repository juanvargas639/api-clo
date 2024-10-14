import requests

def get_rooms(auth_instance, group_id):
    """
    Obtiene los rooms utilizando el token de autenticación.
    
    :param auth_instance: Instancia de la clase Auth.
    :param group_id: ID del grupo del cual se desean obtener los rooms.
    :return: Lista de rooms.
    """
    url = "https://www.clo-set.com/api/rooms"
    headers = auth_instance.get_auth_header()
    headers["Content-Type"] = "application/json"

    # Agregar el groupId como parámetro de consulta a la URL
    params = {"groupId": group_id}

    # Realiza la solicitud GET a la API de CLO para obtener los rooms
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        # Si la respuesta es exitosa, retorna los datos de los rooms
        return response.json()
    else:
        # Si ocurre un error, procesa y devuelve solo el código y mensaje
        try:
            error_data = response.json()
            code = error_data.get("code", "Sin código")
            message = error_data.get("message", "Sin mensaje")
        except ValueError:
            # Si la respuesta de error no es JSON
            code = response.status_code
            message = response.text or "Error desconocido"
        raise Exception(f"Error {code} - {message}")

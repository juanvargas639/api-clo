import requests

def get_categories(auth_instance, company_id):
    """
    Obtiene las categorías para una compañía específica.
    """
    url = f"https://www.clo-set.com/api/categories?companyId={company_id}"
    headers = auth_instance.get_auth_header()
    headers["Content-Type"] = "application/json"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Devuelve la lista de categorías
    else:
        try:
            error_data = response.json()
            code = error_data.get("code", "Sin código")
            message = error_data.get("message", "Sin mensaje")
        except ValueError:
            code = response.status_code
            message = response.text or "Error desconocido"
        raise Exception(f"Error {code} - {message}")

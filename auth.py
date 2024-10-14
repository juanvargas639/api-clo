import requests
import time

## Clase de Autenticación
class Auth:
    def __init__(self, email, password, api_version="2.0"):
        self.email = email
        self.password = password
        self.api_version = api_version
        self.token = None
        self.token_expiration = None
        self.token_url = "https://www.clo-set.com/api/auth/token"
        self.estimated_expiration_time = 1209600  # 14 días en segundos
    
    def get_token(self):
        """
        Solicita un nuevo token si el token actual es nulo o ha expirado.
        """
        if not self.token or time.time() >= self.token_expiration:
            print("Solicitando nuevo token...")
            response = requests.post(
                self.token_url,
                headers={"api-version": self.api_version},
                json={"email": self.email, "password": self.password}
            )
            
            if response.status_code == 200:
                # El token se recibe como texto simple
                self.token = response.text.strip()
                # Asumimos un tiempo de expiración estimado de 14 días
                self.token_expiration = time.time() + self.estimated_expiration_time
                print("Token obtenido exitosamente.")
            else:
                # Procesar y devolver el código de error y el mensaje
                try:
                    error_data = response.json()
                    code = error_data.get("code", "Sin código")
                    message = error_data.get("message", "Sin mensaje")
                except ValueError:
                    # Si la respuesta de error no es JSON
                    code = response.status_code
                    message = response.text or "Error desconocido"
                raise Exception(f"Error {code} - {message}")
        
        return self.token

    def get_auth_header(self):
        """
        Retorna el header de autenticación con el token actual.
        """
        token = self.get_token()
        return {"Authorization": f"Bearer {token}", "api-version": self.api_version}

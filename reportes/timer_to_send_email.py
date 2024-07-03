""" Azure Function para enviar correos electrónicos a los usuarios. """
import logging
import requests
from .constants import API_BASE_URL

def timer_to_send_email(request):
    """Azure Function para enviar correos electrónicos a los usuarios."""
    try:
        # Obtener la URL base desde las variables de entorno
        if not API_BASE_URL:
            raise ValueError("La variable de entorno API_BASE_URL no está definida.")

        api_url = f"{API_BASE_URL}/send_next_email/"

        # Realiza la solicitud POST utilizando requests
        response = requests.post(api_url, timeout=5)
        if response.status_code == 200:
            print('Solicitud POST exitosa')
        else:
            print(f'Error en la solicitud POST: {response.status_code}')

        # Log de éxito
        logging.info('Solicitud POST exitosa: %s', response.status_code)
        return response.status_code

    except requests.exceptions.RequestException as e:
        logging.error('Error en la solicitud POST', exc_info=e)
        return None
    finally:
        logging.info('Python timer trigger function executed.')

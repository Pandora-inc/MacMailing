""" Azure Function App to send email to the next user in the queue. """
import http.client
import logging

API_HOST = "http://macmailling.eastus.cloudapp.azure.com:8000"
API_PATH = "send_next_email/"

conn = http.client.HTTPSConnection(API_HOST)
conn.request("POST", API_PATH)

response = conn.getresponse()

if response.status in (200, 208):
    logging.info('Solicitud POST exitosa')
else:
    logging.info('Error en la solicitud POST: %s', response.status)

logging.info('Python timer trigger function executed.')

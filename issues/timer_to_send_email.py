import http.client
import logging

api_host = "http://macmailling.eastus.cloudapp.azure.com:8000"
api_path = "send_next_email/"
conn = http.client.HTTPSConnection("http://macmailling.eastus.cloudapp.azure.com:8000")
conn.request("POST", "send_next_email/")
response = conn.getresponse()
if response.status == 200 or response.status == 208:
   logging.info('Solicitud POST exitosa')
else:
   logging.info('Error en la solicitud POST: response.status_code')
   logging.info(response.status_code)
logging.info('Python timer trigger function executed.')
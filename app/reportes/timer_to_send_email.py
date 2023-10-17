import http.client
import logging

def timer_to_send_email(request):
   try:
      api_host = "http://macmailling.eastus.cloudapp.azure.com:8000"
      api_path = "send_next_email/"
      conn = http.client.HTTPSConnection(api_host)
      print(conn)
      conn.request("POST", api_path)
      response = conn.getresponse()
      if response.status == 200 or response.status == 208:
         logging.info('Solicitud POST exitosa')
      else:
         logging.info('Error en la solicitud POST: response.status_code')
         logging.info(response.status)
   except Exception as e:
      logging.info('Error en la solicitud POST: response.status_code')
      logging.info(e)
   logging.info('Python timer trigger function executed.')
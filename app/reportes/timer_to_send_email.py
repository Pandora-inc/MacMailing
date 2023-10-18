import http.client
import logging
import requests
import urllib.request

def timer_to_send_email(request):
   try:
      api_host = "http://macmailling.eastus.cloudapp.azure.com:8000"
      api_path = "send_next_email"

         
      # Realiza la solicitud POST
      response = requests.post(api_host+'/'+api_path)

      if response.status_code == 200:
         print(f'Solicitud POST exitosa a las ')
      else:
         print(f'Error en la solicitud POST: {response.status_code} a las ')

      req = urllib.request.Request(api_host+'/'+api_path, method='POST')
    
      try:
         with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            print(f'Solicitud POST exitosa a las . Respuesta: {response_data}')
      except Exception as e:
         print(f'Error en la solicitud POST: {str(e)} a las ')


      conn = http.client.HTTPSConnection(api_host)
      print(conn)
      conn.request("POST", api_path, headers={"Host": api_host})
      print(conn)
      response = conn.getresponse()
      if response.status == 200 or response.status == 208:
         logging.info('Solicitud POST exitosa')
      else:
         logging.info('Error en la solicitud POST: response.status_code')
         logging.info(response.status)
      return http.client.responses[response.status]
   except Exception as e:
      print('Error en la solicitud POST')
      print(e)
   logging.info('Python timer trigger function executed.')
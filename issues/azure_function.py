import logging
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=True) 
def timer_to_send_mail(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    api_url = "http://macmailling.eastus.cloudapp.azure.com:8000/send_next_email/"
    
    # Realiza la solicitud POST
    func.HttpRequest(url=api_url, method='POST', headers=None, body=None, params=None, 
                     route_params=None)
    # if response.status_code == 200 or response.status_code == 208:
    logging.info('Solicitud POST exitosa')
    # else:
    #    logging.info('Error en la solicitud POST: response.status_code')
    #    logging.info(response.status_code)

    logging.info('Python timer trigger function executed.')

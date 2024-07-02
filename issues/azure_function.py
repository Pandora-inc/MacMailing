""" Azure Function que se ejecuta cada 5 minutos para enviar correos electrónicos. """
import logging
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 */5 * * * *", arg_name="my_timer", run_on_startup=True,
              use_monitor=True)
def timer_to_send_mail(my_timer: func.TimerRequest) -> None:
    """ Azure Function que se ejecuta cada 5 minutos para enviar correos electrónicos. """
    if my_timer.past_due:
        logging.info('The timer is past due!')

    api_url = "http://macmailling.eastus.cloudapp.azure.com:8000/send_next_email/"

    # Realiza la solicitud POST
    func.HttpRequest(url=api_url, method='POST', headers=None, body=None, params=None,
                     route_params=None)
    logging.info('Solicitud POST exitosa')

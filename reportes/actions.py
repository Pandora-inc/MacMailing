""" This module contains functions to send emails and update the database. """
# imports de bibliotecas estándar y terceros
import smtplib
import ssl
import string
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import timedelta, datetime
import certifi
import requests

# imports de Django y Django Rest Framework
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, transaction
from django.http import Http404, JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# imports específicos de tu aplicación
from calendarapp.models import Event
from reportes.utils import send_log_message
from reportes.models import (Clientes, ClientesEmail, Mail, TemplateFiles, MailsToSend)
from reportes.serializers import MailSerializer
from reportes.constants import BITRIX_BASE_URL, BITRIX_WEBHOOK

PRE_URL = str(Path(__file__).resolve().parent.parent)
PRE_URL = PRE_URL+'/'

def crear_evento(mail: Mail):
    """
    Creates or updates an event in the calendar app based on the
    information provided in a 'Mail' object.

    Args:
        mail (Mail): The 'Mail' object containing information about the email sent.

    Returns:
        None

    Raises:
        None

    """
    try:
        title = str(mail.send_number) + ' - ' + str(mail.subject)
        description = "Recordatorio envio de mail Nro "+str(mail.send_number)
        if timezone.is_naive(mail.last_send):
            mail.last_send = timezone.make_aware(mail.last_send, timezone.get_default_timezone())
        start_time = mail.last_send+timedelta(days=mail.reminder_days)
        end_time = start_time+timedelta(hours=1)
        # user = User.objects.get(id=mail.mail_corp.user.id)
        connection.cursor()

        if Event.objects.filter(title=title).exists():
            send_log_message ("Evento ya existe")
            event = Event.objects.get(title=title)
            event.description = description
            event.start_time = start_time
            event.end_time = end_time
            event.save()
        else:
            Event.objects.create(
                user=mail.mail_corp.user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
            )
    except Exception as e_error:
        send_log_message(type(e_error))
        send_log_message("Error al crear el evento")
        send_log_message(e_error)
        raise e_error

    send_log_message("Evento creado")

def actualizar_con_template(id_mail: int):
    """
    Updates an email with a template.

    Retrieve the email object based on the provided id_mail.
    Check if a template exists for the email's template group and send number.
    If a template exists, retrieve the template object.
    Update the email's body with the template's text and subject with the template's name.
    Save the updated email object.
    If no template is found, set the email's status to 0.
    Handle exceptions if the email does not exist or if there is an error during the update process.

    Args:
        id_mail (int): The ID of the email to be updated.

    Raises:
        Http404: If the email with the given ID does not exist.
        Exception: If there is an error while updating the email with the template.

    Returns:
        None

    """
    try:
        mail = Mail.objects.get(id=id_mail)
        number = mail.send_number+1
        template_group = mail.template_group

        while template_group.max_number < number:
            number = number - template_group.max_number
            if number == template_group.max_number:
                break

        if TemplateFiles.objects.filter(template_group_id=mail.template_group,
                                        orden=number).exists():
            template = TemplateFiles.objects.get(template_group_id=mail.template_group,
                                                 orden=number)
            mail.body = template.text
            mail.subject = template.name
            mail.save()
        else:
            mail.status = 0
            mail.save()
    except Mail.DoesNotExist as exc:
        send_log_message("Error al actualizar el mail con el template")
        send_log_message("No existe el mail")
        raise Http404 from exc
    except Exception as e_error:
        send_log_message("Error al actualizar el mail con el template")
        send_log_message(e_error)
        raise e_error

def registro_envio_mail(id_mail: int, send_number: int):
    """
    Update the status of a sent email in the database and create or update an
    event in the calendar app.

    Args:
        id_mail (int): The id of the email to be updated in the database.
        send_number (int): The number of times the email has been sent.

    Returns:
        None

    Additional aspects:
        - This function requires the 'crear_evento' function to be defined
            and imported in the module.
        - The function uses the Django ORM to retrieve the 'Mail' object
            associated with the 'id_mail' input.
    """
    with connection.cursor():
        try:
            mail = Mail.objects.get(id=id_mail)
            mail.status = 1
            mail.send_number = send_number
            now = datetime.now()
            if timezone.is_naive(now):
                now = timezone.make_aware(now, timezone.get_default_timezone())
            mail.last_send = now
            mail.save()

            crear_evento(mail)

            if mail.send_number == 1:
                actualizar_con_template(id_mail)
                actualizacion = actualizar_status_bitrix(mail)
                if actualizacion.status_code != 200:
                    send_log_message("Error al actualizar el estado del mail en Bitrix")
                    send_log_message(f"Error: {actualizacion.status_code}")
                    send_log_message(actualizacion.data)
                else:
                    send_log_message("Registro actualizado en bitrix")

            send_log_message("Registro de envio de mail actualizado")
        except Mail.DoesNotExist as e_error:
            send_log_message("Error al actualizar el registro de envio de mail")
            send_log_message("No existe el mail")
            raise e_error
        except Exception as e_error:
            send_log_message("Error al actualizar el registro de envio de mail")
            send_log_message(e_error)
            raise e_error

def actualizar_status_bitrix(mail: Mail):
    """
    Update the status of a lead in Bitrix CRM.

    Parameters:
        mail (Mail): The email object containing the lead information.

    Returns:
        Response: A response object indicating the success or failure of the status update.

    Raises:
        Exception: If an error occurs during the status update process.

    """
    try:
        send_log_message("Actualizando estado del mail en Bitrix")
        send_log_message(mail.cliente.cliente_id)
        url = f'{BITRIX_BASE_URL}/{BITRIX_WEBHOOK}/crm.lead.update.json'
        data = {
            'ID': mail.cliente.cliente_id,
            'fields': {
                'ID': mail.cliente.cliente_id,
                'STATUS_ID': 'IN_PROCESS'
            },
            'params': {
                'REGISTER_SONET_EVENT': 'Y'
            }
        }

        response = requests.post(url, json=data, timeout=5)
        if response.status_code != 200:
            send_log_message(str(data))

        return Response(response.json(), status=response.status_code)
    except Exception as e_error:
        send_log_message("Error al actualizar el estado del mail en Bitrix")
        send_log_message(e_error)
        raise e_error

def prepare_email_body(text: str, data: dict) -> str:
    '''
    Prepara el cuerpo del mail con los datos del cliente.
    Reemplaza las variables {{}} por los datos del cliente.
    '''
    for key, value in data.items():
        text = text.replace('{{'+key+'}}', str(value))
    return text


def get_mail_data(id_mail: int) -> dict:
    '''
    Obtiene los datos del mail a enviar.
    '''
    try:
        mail = Mail.objects.get(id=id_mail)
        return get_data_for_mail(mail)
    except Mail.DoesNotExist as e_error:
        send_log_message("Error when obtaining the data of the mail to be sent.")
        send_log_message("Mail does not exist")
        raise e_error

def get_data_for_mail(mail: Mail, next_mail_id: int=None) -> dict:
    '''
    Obtiene los datos del mail a enviar.
    '''
    try:
        mail_corp = mail.mail_corp
        cliente = mail.cliente
        if cliente:  # Asegúrate de que cliente no sea None
            cliente_email = ClientesEmail.objects.filter(cliente=cliente, type=1).first()
            if cliente_email:  # Asegúrate de que cliente_email no sea None
                data = {
                    'subject': mail.subject,
                    'from_name': mail_corp.name,
                    'from_email': mail_corp.email,
                    'to': cliente_email.data,
                    'date': datetime.now().isoformat(),
                    'content': mail.body,
                    'number': mail.send_number,
                    'content_type': 'text/html',
                    'from_pass': mail_corp.password,
                    'from_smtp': mail_corp.smtp,
                    'from_port': mail_corp.smtp_port,
                    'salutation': cliente.salutation,
                    'first_name': cliente.first_name,
                    'middle_name': cliente.middle_name,
                    'last_name': cliente.last_name,
                    'lead_name': cliente.lead_name,
                    'data': cliente_email.data,
                    'company_name': cliente.company_name,
                    'position': cliente.position,
                    'type': cliente.type.name,
                    'firma': mail_corp.firma,
                    'user_name': mail_corp.user.first_name,
                    'user_last_name': mail_corp.user.last_name,
                    'mail_id': mail.id,
                }

                if cliente.source_information:
                    data['cc'] = emails_cadena(cliente.source_information)

                if next_mail_id:
                    data['mail_to_send_id'] = next_mail_id
                else:
                    data['mail_to_send_id'] = MailsToSend.objects.filter(mail=mail,
                                                                        send=False).first().id

                serializer = MailSerializer(data=data)
                if serializer.is_valid():
                    return serializer.data

                send_log_message(f"Lead: {cliente}")
                send_log_message("Error al obtener los datos del mail a enviar.")
                send_log_message(serializer.errors)
                return serializer.errors

        send_log_message("El mail no tiene un cliente asociado.")
        return None
    except ClientesEmail.DoesNotExist as e_error:
        send_log_message("Error when obtaining the data of the mail to send.")
        send_log_message("No customer_email with type=1 was found for the customer.")
        raise e_error

def add_image_to_email(content: str, message: MIMEMultipart) -> str:
    """ Función que localiza y formatea las imágenes que se encuentran en el contenido del mail. """
    inicio = content.find('src="/media/uploads')
    try:
        if inicio != -1:
            imagen_url = content.replace('/media/', '/static_media/')
            fin = imagen_url.find('"', inicio+5)
            imagen_url = imagen_url[inicio+6:fin]
            imagen_url_original = imagen_url.replace('static_media/', 'media/')
            imagen_name = imagen_url[imagen_url.rfind('/')+1:]
            content = content.replace(
                '/'+imagen_url_original, 'cid:'+imagen_name[:imagen_name.find('.')])

            imagen_url = PRE_URL+imagen_url

            with open(imagen_url, 'rb') as file:
                image = MIMEImage(file.read())
                image.add_header('Content-ID', '<' +
                                imagen_name[:imagen_name.find('.')]+'>')
                message.attach(image)
        return content
    except FileNotFoundError as e_error:
        send_log_message("Error al agregar la imagen al mail")
        send_log_message(e_error)
        raise e_error
    except Exception as e_error:
        send_log_message("Error al agregar la imagen al mail")
        send_log_message(e_error)
        raise e_error

def register_first_email(id_mail: int):
    """
    Register the first email sent to a client.

    Args:
        id_mail (int): The ID of the email to register.

    Raises:
        Mail.DoesNotExist: If the email with the given ID does not exist.
        Clientes.DoesNotExist: If the client associated with the email does not exist.

    """
    try:
        mail = Mail.objects.get(id=id_mail)
        if mail.send_number == 1:
            cliente = Clientes.objects.get(id=mail.cliente.id)
            cliente.contacted = True
            cliente.contacted_on = datetime.now()
            cliente.save()
    except Mail.DoesNotExist as e_error:
        send_log_message("Error al registrar el primer mail")
        send_log_message("No existe el mail")
        raise e_error
    except Clientes.DoesNotExist as e_error:
        send_log_message("Error al registrar el primer mail")
        send_log_message("No existe el cliente")
        raise e_error
    except Exception as e_error:
        send_log_message("Error al registrar el primer mail")
        send_log_message(e_error)
        raise e_error


def send_mail(id_mail: int) -> bool:
    """
    Sends an email with the given id_mail.

    Args:
        id_mail (int): The id of the email to be sent.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    msg_data = get_mail_data(id_mail)
    if send_new_mail(msg_data):
        return True
    return False

def send_mail_api(request, id_mail: int) -> bool:
    """
    Sends an email with the given id_mail.

    Args:
        id_mail (int): The id of the email to be sent.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    msg_data = get_mail_data(id_mail)
    send_new_mail(msg_data)


def get_template_file_and_save(id_template: int) -> bool:
    """
    Retrieves a template file from the database, reads its contents,
    and saves the contents as text in the same template object.

    Args:
        id_template (int): The ID of the template file to retrieve from the database.

    Returns:
        None
    """
    template = TemplateFiles.objects.get(id=id_template)
    try:
        filename = template.file
        if filename:
            with open(filename, "r", encoding="utf-8") as archivo:
                template.text = archivo.read()
                template.save()
                return True
        return False
    except FileNotFoundError as e_error:
        send_log_message("Error al leer el archivo")
        send_log_message(e_error)
        raise e_error
    except FileExistsError as e_error:
        send_log_message("Error al leer el archivo")
        send_log_message(e_error)
        raise e_error


def emails_cadena(cadena):
    """ Función que extrae todos los emails válidos de una cadena de texto. """
    try:
        caracteres_puntuacion = string.punctuation.replace('@', '').replace('.', '')
        traductor = str.maketrans("", "", caracteres_puntuacion)
        cadena_sin_puntuacion = cadena.translate(traductor)
        palabras = cadena_sin_puntuacion.lower().split()
        emails = []
        for palabra in palabras:
            if "@" in palabra:
                partes_email = palabra.split("@")
                # Verificamos que haya exactamente una arroba en el correo
                if len(partes_email) == 2:
                    _, dominio = partes_email
                    # Verificamos que haya un punto después de la arroba en el dominio
                    if "." in dominio:
                        # Añadimos el email a la lista de emails válidos
                        emails.append(palabra)
                    else:
                        send_log_message(f"The domain of the email '{palabra}' is not valid.")
                else:
                    send_log_message(f"The email '{palabra}' contains more than one arroba.")
        # Si no se encontraron emails válidos, mostramos un mensaje
        if len(emails) == 0:
            send_log_message("No valid emails were found in the string.")
            return None
        return emails
    except ValueError as error:
        send_log_message(f"Error processing string: {error}")
        raise error


def get_next_email_data() -> dict:
    '''
    Obtiene los datos del mail a enviar.
    '''
    try:
        next_mail = MailsToSend.objects.filter(approved=True,
                                           send=False).order_by('date_approved').first()

        if next_mail:  # Asegúrate de que mail no sea None
            send_log_message(f"Next mail to send: {next_mail.id}")
            return get_data_for_mail(next_mail.mail, next_mail.id)
    except MailsToSend.DoesNotExist:
        send_log_message("No email found to send.")
        return None

def send_new_mail(msg_data) -> JsonResponse:
    """
    Sends a new email using the provided message data.

    Args:
        msg_data (dict): A dictionary containing the necessary data for
            sending the email. It should have the following keys:
            - 'from_email' (str): The email address of the sender.
            - 'To' (str): The email address of the recipient.
            - 'Subject' (str): The subject of the email.
            - 'CC' (str): The email addresses to be included in the CC field.
            - 'content' (str): The content of the email.
            - 'firma' (str): The signature of the email.
            - 'mail_to_send_id' (int): The ID of the mail to be sent.
            - 'from_smtp' (str): SMTP server address.
            - 'from_port' (int): SMTP server port.
            - 'from_pass' (str): Sender's email password.

    Returns:
        JsonResponse: JSON response indicating success or failure.

    Raises:
        ObjectDoesNotExist: If the mail with the given ID does not exist.
        Exception: If there is an error in the process of sending the email.

    Additional aspects:
        - This function uses the 'prepare_email_body' function to prepare
            the email body by replacing variables with client data.
        - This function uses the 'add_image_to_email' function to locate and
            format images in the email content.
        - This function uses the Django ORM to retrieve the 'MailsToSend' object
            associated with the 'mail_to_send_id' input.
        - This function uses the 'register_envio_mail' function to update the status
             of the sent email in the database and create or update an event in the calendar app.
        - This function uses the 'register_first_email' function to register the first
            email sent to a client.
    """

    try:
        message = MIMEMultipart()

        send_log_message(f"Buscando el mensaje: {msg_data['mail_to_send_id']}")
        mail_to_send = MailsToSend.objects.get(id=msg_data['mail_to_send_id'])

        message['From'] = msg_data['from_email']
        message['To'] = msg_data['to']
        message['Subject'] = msg_data['subject']
        if msg_data['cc']:
            message['CC'] = ', '.join(msg_data['cc'])
            if message['CC'] is None:
                send_log_message("sin cc")
                message['CC'] = ''


        msg_data['content'] = prepare_email_body(msg_data['content'], msg_data)
        msg_data['firma'] = prepare_email_body(msg_data['firma'], msg_data)

        msg_data['content'] = add_image_to_email(msg_data['content'], message)
        msg_data['firma'] = add_image_to_email(msg_data['firma'], message)

        content = msg_data['content'] + msg_data['firma']
        message.attach(MIMEText(content, "html"))
        mail = Mail.objects.get(id=msg_data['mail_id'])

        number = mail.send_number+1
        while mail.template_group.max_number < number:
            number = number - mail.template_group.max_number
            if number == mail.template_group.max_number:
                break

        send_log_message(f"order: {number}")
        send_log_message(f"group: {mail.template_group}")

        attachments = TemplateFiles.objects.get(
                                                orden=number,
                                                template_group=mail.template_group
                                                ).attachment.all()
        for attachment in attachments:
            with open(PRE_URL + 'static_media/' + str(attachment.file), 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                filename = attachment.name + "." + str(attachment.file).split(".", maxsplit=1)[-1]
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                message.attach(part)

        # Send email using SMTP
        context = ssl.create_default_context(cafile=certifi.where())
        with smtplib.SMTP(msg_data['from_smtp'], msg_data['from_port']) as server:
            server.starttls(context=context)
            server.login(msg_data['from_email'], msg_data['from_pass'])
            server.send_message(message)

        # Update mail object status and save
        with transaction.atomic():
            mail_to_send.send = True
            mail_to_send.save()

            # Register email sending and first email
            registro_envio_mail(msg_data['mail_id'], msg_data['number'] + 1)
            register_first_email(msg_data['mail_id'])

        return JsonResponse({'mail_id': msg_data['mail_id']}, status=200)

    except ObjectDoesNotExist as e_error:
        error_msg = f"Mail with ID {msg_data['mail_to_send_id']} does not exist."
        mail_to_send.error_message = error_msg
        mail_to_send.approved = False
        mail_to_send.save()
        send_log_message(error_msg)
        return JsonResponse({'code': e_error, 'error': error_msg}, status=404)

    except smtplib.SMTPException as e:
        error_msg = f"Error sending email: {e}"
        mail_to_send.status = False
        mail_to_send.error_message = error_msg
        mail_to_send.approved = False
        mail_to_send.save()
        send_log_message(error_msg)
        return JsonResponse({'error': error_msg}, status=500)

    except KeyError as error:
        error_msg = f"Error in the message data: {error}"
        mail_to_send.status = False
        mail_to_send.error_message = error_msg
        mail_to_send.approved = False
        mail_to_send.save()
        send_log_message(f"Mail to: {msg_data['to']}")
        send_log_message(error_msg)
        return JsonResponse({'error': error_msg}, status=500)

class EmailAPI(APIView):
    """
    API endpoint that allows emails to be sent.
    """
    @api_view(['POST'])
    def send_next_mail(self) -> Response:
        """
        Sends an email with the given id_mail.

        Args:
            id_mail (int): The id of the email to be sent.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        msg_data = get_next_email_data()

        if msg_data is None:
            return Response(status=status.HTTP_208_ALREADY_REPORTED)

        return send_new_mail(msg_data)


    def get_object(self, pk):
        """
        Get the email object with the specified primary key (pk).

        Args:
            pk (int): The primary key of the email object.

        Returns:
            dict: A dictionary containing the email data with the following keys:
                - 'Subject': The subject of the email.
                - 'From': The sender of the email.
                - 'To': The recipient of the email.
                - 'Date': The date of the email.
                - 'content-type': The content type of the email.
                - 'content': The content of the email.
                - 'number': The number of the email.
                - 'from_email': The sender's email address.
                - 'from_pass': The sender's email password.
                - 'from_smtp': The SMTP server for sending the email.
                - 'from_port': The port number for the SMTP server.
                - 'salutation': The salutation in the email.
                - 'first_name': The first name of the recipient.
                - 'middle_name': The middle name of the recipient.
                - 'last_name': The last name of the recipient.
                - 'lead_name': The lead name in the email.
                - 'data': The data in the email.
                - 'company_name': The company name in the email.
                - 'position': The position in the email.
                - 'type': The type of the email.
                - 'firma': The signature in the email.
                - 'user_name': The user's name in the email.
                - 'user_last_name': The user's last name in the email.
                - 'CC': The CC recipients of the email, separated by commas.
                    Empty string if no CC recipients.

        Raises:
            Http404: If the email object with the specified primary key does not exist.
        """
        try:
            return Mail.objects.get(pk=pk)
        except Mail.DoesNotExist as exc:
            raise Http404 from exc

    def get(self, request, pk):
        """ Get the email object with the specified primary key (pk). """
        mail = self.get_object(pk)
        serializer = MailSerializer(mail)
        return Response(serializer.data)

    def put(self, request, pk):
        """ Update the email object with the specified primary key (pk). """
        mail = self.get_object(pk)
        serializer = MailSerializer(mail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """ Create a new email object. """
        serializer = MailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

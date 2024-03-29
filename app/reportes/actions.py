
from datetime import timedelta, datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate
from email import encoders
from pathlib import Path
import string
import smtplib
import ssl
from reportes.serializers import MailSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import Http404
from django.db import connection
from django.contrib.auth import get_user
from calendarapp.models import Event
from reportes.models import Clientes, Mail, TemplateFiles, MailsToSend


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
        start_time = mail.last_send+timedelta(days=mail.reminder_days)
        end_time = start_time+timedelta(hours=1)
        # user = User.objects.get(id=mail.mail_corp.user.id)
        connection.cursor()

        if Event.objects.filter(title=title).exists():
            print ("Evento ya existe")
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
        print(type(e_error))
        print("Error al crear el evento")
        print(e_error)
        raise e_error

    print("Evento creado")

def actualizar_con_template(id_mail: int):
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
        mail = Mail.objects.get(id=id_mail)
        if TemplateFiles.objects.filter(template_group_id=mail.template_group, orden=mail.send_number+1).exists():
            template = TemplateFiles.objects.get(template_group_id=mail.template_group, orden=mail.send_number+1)
            mail.body = template.text
            mail.subject = template.name
            mail.save()
    except Mail.DoesNotExist:
        print("Error al actualizar el mail con el template")
        print("No existe el mail")
        raise Http404
    except Exception as e_error:
        print("Error al actualizar el mail con el template")
        print(e_error)
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
            mail.last_send = datetime.now()
            mail.save()

            crear_evento(mail)

            actualizar_con_template(id_mail)
            print("Registro de envio de mail actualizado")
        except Mail.DoesNotExist as e_error:
            print("Error al actualizar el registro de envio de mail")
            print("No existe el mail")
            raise e_error
        except Exception as e_error:
            print("Error al actualizar el registro de envio de mail")
            print(e_error)
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
    with connection.cursor() as cursor:
        cursor.callproc("get_mail_data", [id_mail])
        row = cursor.fetchone()

        msg = {}
        msg['Subject'] = row[0]
        msg['From'] = row[5]
        msg['To'] = row[16]
        msg['Date'] = formatdate(localtime=True)
        msg['content-type'] = 'text/html'
        msg['content'] = row[1]
        msg['number'] = row[3]
        msg['from_email'] = row[6]
        msg['from_pass'] = row[7]
        msg['from_smtp'] = row[8]
        msg['from_port'] = row[9]
        msg['salutation'] = row[10]
        msg['first_name'] = row[11]
        msg['middle_name'] = row[12]
        msg['last_name'] = row[13]
        msg['lead_name'] = row[14]
        msg['data'] = row[16]
        msg['company_name'] = row[17]
        msg['position'] = row[18]
        msg['type'] = row[19]
        msg['firma'] = row[20]

        msg['user_name'] = row[21]
        msg['user_last_name'] = row[22]
        msg['mail_id'] = row[23]
        msg['mail_to_send_id'] = row[24]

        if row[15]:
            mails = emails_cadena(row[15])
            if mails:
                msg['CC'] = ', '.join(mails)
            else:
                msg['CC'] = ''
        else:
            msg['CC'] = ''

        return msg

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
        print("Error al agregar la imagen al mail")
        print(e_error)
        raise e_error
    except Exception as e_error:
        print("Error al agregar la imagen al mail")
        print(e_error)
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
        print("Error al registrar el primer mail")
        print("No existe el mail")
        raise e_error
    except Clientes.DoesNotExist as e_error:
        print("Error al registrar el primer mail")
        print("No existe el cliente")
        raise e_error
    except Exception as e_error:
        print("Error al registrar el primer mail")
        print(e_error)
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

    message = MIMEMultipart()
    message['From'] = msg_data['from_email']
    message['To'] = msg_data['To']
    message['Subject'] = msg_data['Subject']
    message['cc'] = msg_data['CC']

    msg_data['content'] = prepare_email_body(msg_data['content'], msg_data)
    msg_data['firma'] = prepare_email_body(msg_data['firma'], msg_data)

    msg_data['content'] = add_image_to_email(msg_data['content'], message)
    msg_data['firma'] = add_image_to_email(msg_data['firma'], message)

    content = msg_data['content']+msg_data['firma']

    message.attach(MIMEText(content, "html"))

    with connection.cursor() as cursor:
        consulta_attachment = f"SELECT * FROM reportes_mail_attachment \
                                    INNER JOIN reportes_attachment ON reportes_attachment.id = reportes_mail_attachment.attachment_id \
                                    WHERE mail_id = {id_mail}"
        cursor.execute(consulta_attachment)
        attachment = cursor.fetchall()

        for f in attachment:
            with open(PRE_URL+'static_media/'+f[5], 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={f[4]+"."+f[5].split(".")[-1]}')
                message.attach(part)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(msg_data['from_smtp'], msg_data['from_port']) as server:
            server.starttls(context=context)
            try:
                server.login(msg_data['from_email'], msg_data['from_pass'])
            except Exception as e_error:
                print("Error en el loggeo")
                server.quit()
                raise e_error
            try:
                server.send_message(message)
                server.quit()
                registro_envio_mail(id_mail, msg_data['number']+1)
                register_first_email(id_mail)
                return True
            except Exception as e_error:
                print("Error en el envio del mail")
                server.quit()
                raise e_error
    except Exception as e_error:
        print("Error en la conexión con el servidor")
        print(e_error)
        raise e_error

def send_mail_api(request, id_mail: int) -> bool:
    """
    Sends an email with the given id_mail.

    Args:
        id_mail (int): The id of the email to be sent.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    msg_data = get_mail_data(id_mail)

    message = MIMEMultipart()
    message['From'] = msg_data['from_email']
    message['To'] = msg_data['To']
    message['Subject'] = msg_data['Subject']
    message['cc'] = msg_data['CC']

    msg_data['content'] = prepare_email_body(msg_data['content'], msg_data)
    msg_data['firma'] = prepare_email_body(msg_data['firma'], msg_data)

    msg_data['content'] = add_image_to_email(msg_data['content'], message)
    msg_data['firma'] = add_image_to_email(msg_data['firma'], message)

    content = msg_data['content']+msg_data['firma']

    message.attach(MIMEText(content, "html"))

    with connection.cursor() as cursor:
        consulta_attachment = f"SELECT * FROM reportes_mail_attachment \
                                    INNER JOIN reportes_attachment ON reportes_attachment.id = reportes_mail_attachment.attachment_id \
                                    WHERE mail_id = {id_mail}"
        cursor.execute(consulta_attachment)
        attachment = cursor.fetchall()

        for f in attachment:
            with open(PRE_URL+'static_media/'+f[5], 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={f[4]+"."+f[5].split(".")[-1]}')
                message.attach(part)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(msg_data['from_smtp'], msg_data['from_port']) as server:
            server.starttls(context=context)
            try:
                server.login(msg_data['from_email'], msg_data['from_pass'])
            except Exception as e_error:
                print("Error en el loggeo")
                server.quit()
                raise e_error
            try:
                server.send_message(message)
                server.quit()
                registro_envio_mail(id_mail, msg_data['number']+1)
                register_first_email(id_mail)
                return True
            except Exception as e_error:
                print("Error en el envio del mail")
                server.quit()
                raise e_error
    except Exception as e_error:
        print("Error en la conexión con el servidor")
        print(e_error)
        raise e_error

def get_template_file_and_save(id_template: int):
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
        filename = template.file.path

        with open(filename, "r", encoding="utf-8") as archivo:
            template.text = archivo.read()
            template.save()
    except Exception as e_error:
        print("Error al leer el archivo")
        print(e_error)
        raise e_error


def emails_cadena(cadena):
    """ Función que nos servirá para extraer todos los email válidos de una cadena de texto. """
    try:
        # Definimos una lista de signos de puntuación a eliminar, excepto @ y .
        caracteres_puntuacion = string.punctuation.replace(
            '@', '').replace('.', '').replace('_', '').replace('-', '')

        # Eliminamos todos los caracteres de puntuación de la cadena,
        # que no se usan en los correos electrónicos
        traductor = str.maketrans("", "", caracteres_puntuacion)
        cadena_sin_puntuacion = cadena.translate(traductor)

        # Dividimos la cadena con el método .split() convirtiéndola en una lista
        cad = cadena_sin_puntuacion.lower().split()
        # Creamos una lista vacía
        emails = []

        for correo in cad:
            try:
                if "@" in correo:
                    # Almacenamos el índice de la arroba
                    indice_arroba = correo.index("@")

                    # Se produce una excepción si hay más de una arroba e el email
                    if correo.count("@") > 1:
                        raise ValueError(
                            "Hay más de una arroba en el e-mail: " + correo)

                    # eliminamos los espacios en blanco del correo
                    correo_limpio = correo.replace(" ", "")

                    # si hay un punto después de la arroba dividimos el correo en nombre
                    # (antes de la arroba) y dominio (después de la arroba)
                    if "." in correo_limpio[indice_arroba + 1:]:
                        nombre, dominio = correo.split("@")

                        # si tiene dos o más caracteres, el dominio es válido.
                        # Quitamos los espacios que puedan haber en el dominio
                        # y añadimos el correo (tupla) en la lista 'emails'
                        if len(dominio.split(".")[-1]) > 1:
                            dominio_limpio = dominio.replace(" ", "")
                            emails.append((nombre, dominio_limpio))
                        else:
                            print(
                                f"El dominio del e-mail '{correo}' no es válido")
                    else:
                        print("No has introducido un dominio en el e-mail :", correo)

            # Se muestra la excepción en caso de haber más de una arroba
            except ValueError as e_error:
                print(e_error)

        # Si no hay correos en la lista...
        if len(emails) == 0:
            print("No se encontraron correos electrónicos en la cadena.")
        else:
            # Recorremos la lista y mostramos todos los emails en caso de tener nombre de usuario..,
            response = []
            for email in emails:
                if email[0]:
                    response.append(f"{email[0]}@{email[1]}")
                # de lo contrario se muestra el texto con el nombre del dominio en cuestión
                else:
                    print("No existe  un nombre de usuario en :", email[1])

            return response

    except Exception as e_error:
        print(e_error)
        print("Ha ocurrido un error inesperado al procesar la cadena.")

def get_next_email_data() -> dict:
    '''
    Obtiene los datos del mail a enviar.
    '''
    with connection.cursor() as cursor:
        cursor.callproc("get_next_mail_to_send", [])
        row = cursor.fetchone()

        if row is None:
            return None

        msg = {}
        msg['Subject'] = row[0]
        msg['From'] = row[5]
        msg['To'] = row[16]
        msg['Date'] = formatdate(localtime=True)
        msg['content-type'] = 'text/html'
        msg['content'] = row[1]
        msg['number'] = row[3]
        msg['from_email'] = row[6]
        msg['from_pass'] = row[7]
        msg['from_smtp'] = row[8]
        msg['from_port'] = row[9]
        msg['salutation'] = row[10]
        msg['first_name'] = row[11]
        msg['middle_name'] = row[12]
        msg['last_name'] = row[13]
        msg['lead_name'] = row[14]
        msg['data'] = row[16]
        msg['company_name'] = row[17]
        msg['position'] = row[18]
        msg['type'] = row[19]
        msg['firma'] = row[20]
        msg['user_name'] = row[21]
        msg['user_last_name'] = row[22]
        msg['mail_id'] = row[23]
        msg['mail_to_send_id'] = row[24]

        if row[15]:
            mails = emails_cadena(row[15])
            if mails:
                msg['CC'] = ', '.join(mails)
            else:
                msg['CC'] = ''
        else:
            msg['CC'] = ''

        return msg

class EmailAPI(APIView):
    """
    API endpoint that allows emails to be sent.
    """
    @api_view(['POST'])
    def send_next_mail(self) -> bool:
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

        message = MIMEMultipart()
        message['From'] = msg_data['from_email']
        message['To'] = msg_data['To']
        message['Subject'] = msg_data['Subject']
        message['cc'] = msg_data['CC']

        msg_data['content'] = prepare_email_body(msg_data['content'], msg_data)
        msg_data['firma'] = prepare_email_body(msg_data['firma'], msg_data)

        msg_data['content'] = add_image_to_email(msg_data['content'], message)
        msg_data['firma'] = add_image_to_email(msg_data['firma'], message)

        content = msg_data['content']+msg_data['firma']

        message.attach(MIMEText(content, "html"))
        try:
            with connection.cursor() as cursor:
                cursor.callproc("get_mail_attachment", [msg_data['mail_id']])
                attachment = cursor.fetchall()

                for f in attachment:
                    with open(PRE_URL+'static_media/'+f[5], 'rb') as file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(file.read())
                        encoders.encode_base64(part)
                        filename = f[4]+"."+f[5].split(".")[-1]
                        part.add_header('Content-Disposition', f'attachment; filename={filename}')
                        message.attach(part)
        except Exception as e_error:
            print("Error al obtener los adjuntos")
            print(e_error)

            # respuesta = Response(status=status.HTTP_200_OK)
            respuesta = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                 data="Error con los adjuntos" )
            print(respuesta)
            return respuesta

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(msg_data['from_smtp'], msg_data['from_port']) as server:
                server.starttls(context=context)
                try:
                    server.login(msg_data['from_email'], msg_data['from_pass'])
                except Exception as e_error:
                    print("Error en el loggeo")
                    server.quit()
                    raise e_error
                try:
                    server.send_message(message)
                    server.quit()
                    registro_envio_mail(msg_data['mail_id'], msg_data['number']+1)
                    register_first_email(msg_data['mail_id'])

                    mail_to_send = MailsToSend.objects.get(id=msg_data['mail_to_send_id'])
                    mail_to_send.send = True
                    mail_to_send.save()
                except MailsToSend.DoesNotExist as e_error:
                    print("Error al actualizar el estado del mail a enviar")
                    print("ID del mail a enviar: "+str(msg_data['mail_to_send_id']))
                    server.quit()
                    raise e_error
                except Exception as e_error:
                    print("Error en el envio del mail")
                    server.quit()
                    raise e_error
                else:
                    # respuesta = Response(status=status.HTTP_200_OK)
                    respuesta = Response(status=status.HTTP_200_OK, data={'mail_id': msg_data['mail_id']} )
                    print(respuesta)
                    return respuesta
        except Exception as e_error:
            print("Error en la conexión con el servidor")
            print(e_error)
            raise e_error

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
                - 'CC': The CC recipients of the email, separated by commas. Empty string if no CC recipients.

        Raises:
            Http404: If the email object with the specified primary key does not exist.
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc("get_mail_data", [pk])
                # data = dictfetchall(cursor)
                row = cursor.fetchone()

                msg = {}
                msg['Subject'] = row[0]
                msg['From'] = row[5]
                msg['To'] = row[16]
                msg['Date'] = formatdate(localtime=True)
                msg['content-type'] = 'text/html'
                msg['content'] = row[1]
                msg['number'] = row[3]
                msg['from_email'] = row[6]
                msg['from_pass'] = row[7]
                msg['from_smtp'] = row[8]
                msg['from_port'] = row[9]
                msg['salutation'] = row[10]
                msg['first_name'] = row[11]
                msg['middle_name'] = row[12]
                msg['last_name'] = row[13]
                msg['lead_name'] = row[14]
                msg['data'] = row[16]
                msg['company_name'] = row[17]
                msg['position'] = row[18]
                msg['type'] = row[19]
                msg['firma'] = row[20]

                msg['user_name'] = row[21]
                msg['user_last_name'] = row[22]
                msg['mail_id'] = row[23]
                msg['mail_to_send_id'] = row[24]

                if row[15]:
                    mails = emails_cadena(row[15])
                    if mails:
                        msg['CC'] = ', '.join(mails)
                    else:
                        msg['CC'] = ''
                else:
                    msg['CC'] = ''

                return msg
        except Mail.DoesNotExist as exc:
            raise Http404 from exc

    def get(self, request, pk, format=None):
        mail = self.get_object(pk)
        serializer = MailSerializer(mail)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        mail = self.get_object(pk)
        serializer = MailSerializer(mail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = MailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
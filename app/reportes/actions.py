
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate
import string
import smtplib
import ssl
from django.contrib.auth.models import User
from django.db import connection
from calendarapp.models import Event
from reportes.models import Mail, TemplateFiles


def crear_evento(mail: Mail):
    """
    Creates or updates an event in the calendar app based on the information provided in a 'Mail' object.

    Args:
        mail (Mail): The 'Mail' object containing information about the email sent.

    Returns:
        None

    Raises:
        None

    """
    title = mail.subject
    description = "Recordatorio envio de mail Nro "+str(mail.send_number)
    start_time = mail.last_send+timedelta(days=mail.reminder_days)
    end_time = start_time+timedelta(hours=1)
    # user = User.objects.get(id=mail.mail_corp.user.id)

    print("Creando evento")

    if Event.objects.filter(user=mail.mail_corp.user, title=title).exists():
        event = Event.objects.get(user=mail.mail_corp.user, title=title)
        event.description = description
        event.start_time = start_time
        event.end_time = end_time
        event.save()
    else:
        Event.objects.get_or_create(
            user=mail.mail_corp.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )

    print("Evento creado")


def registro_envio_mail(id_mail: int, send_number: int):
    """
    Update the status of a sent email in the database and create or update an event in the calendar app.

    Args:
        id_mail (int): The id of the email to be updated in the database.
        send_number (int): The number of times the email has been sent.

    Returns:
        None

    Additional aspects:
        - This function requires the 'crear_evento' function to be defined and imported in the module.
        - The function uses the Django ORM to retrieve the 'Mail' object associated with the 'id_mail' input.
    """
    with connection.cursor() as cursor:
        consulta = f"UPDATE reportes_mail SET status = 1, send_number = {send_number}, last_send = NOW() WHERE id = {id_mail}"
        cursor.execute(consulta)
        connection.commit()

        mail = Mail.objects.get(id=id_mail)
        crear_evento(mail)


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
        consulta = f"SELECT \
            reportes_mail.subject, \
            reportes_mail.body, \
            reportes_mail.status, \
            reportes_mail.send_number, \
            reportes_mail.last_send, \
            reportes_mailcorp.name, \
            reportes_mailcorp.email, \
            reportes_mailcorp.password, \
            reportes_mailcorp.smtp, \
            reportes_mailcorp.smtp_port, \
            clientes.salutation, \
            clientes.first_name, \
            clientes.middle_name, \
            clientes.last_name, \
            clientes.lead_name, \
            clientes.source_information, \
            reportes_clientesemail.data, \
            clientes.company_name, \
            clientes.position, \
            auxiliares_type.name \
        FROM \
            reportes_mail \
            INNER JOIN reportes_mailcorp ON reportes_mailcorp.id = reportes_mail.mail_corp_id \
            INNER JOIN clientes ON clientes.id = reportes_mail.cliente_id \
            INNER JOIN reportes_clientesemail ON reportes_clientesemail.cliente_id = reportes_mail.cliente_id \
            INNER JOIN auxiliares_type ON auxiliares_type.id = clientes.type_id \
        WHERE \
            reportes_mail.id = {id_mail} \
            AND reportes_clientesemail.type_id = 1"

        cursor.execute(consulta)
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

        if row[15]:
            msg['CC'] = ', '.join(emails_cadena(row[15]))
        else:
            msg['CC'] = ''

        return msg


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
    message['From'] = msg_data['From']
    message['To'] = msg_data['To']
    message['Subject'] = msg_data['Subject']

    msg_data['content'] = prepare_email_body(msg_data['content'], msg_data)
        

    # Replace the images that come from ckeditor
    inicio = msg_data['content'].find('src="/media/uploads')
    if inicio != -1:
        imagen_url = msg_data['content'].replace('/media/', '/static_media/')
        fin = imagen_url.find('"', inicio+5)
        imagen_url = imagen_url[inicio+6:fin]
        imagen_url_original = imagen_url.replace('static_media/', 'media/')
        imagen_name = imagen_url[imagen_url.rfind('/')+1:]
        msg_data['content'] = msg_data['content'].replace(
            '/'+imagen_url_original, 'cid:'+imagen_name[:imagen_name.find('.')])

        with open(imagen_url, 'rb') as file:
            image = MIMEImage(file.read())
            image.add_header('Content-ID', '<' +
                             imagen_name[:imagen_name.find('.')]+'>')
            message.attach(image)

    message.attach(MIMEText(msg_data['content'], "html"))

    with connection.cursor() as cursor:
        consulta_attachment = f"SELECT * FROM reportes_mail_attachment \
                                    INNER JOIN reportes_attachment ON reportes_attachment.id = reportes_mail_attachment.attachment_id \
                                    WHERE mail_id = {id_mail}"
        cursor.execute(consulta_attachment)
        attachment = cursor.fetchall()

        for f in attachment:
            with open('static_media/'+f[5], 'rb') as file:
                image = MIMEImage(file.read())
                image.add_header('Content-ID', '<'+f[4]+'>')
                message.attach(image)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(msg_data['from_smtp'], msg_data['from_port']) as server:
            server.starttls(context=context)
            try:
                server.login(msg_data['from_email'], msg_data['from_pass'])
                server.send_message(message)
                server.quit()
                registro_envio_mail(id_mail, msg_data['number']+1)
                return True
            except Exception as e_error:
                print("Error en el loggeo y envio del mail")
                print(e_error)
                server.quit()
                return False
    except Exception as e_error:
        print("Error en la conexión con el servidor")
        print("from_smtp: "+msg_data['from_smtp'])
        print("from_port: "+str(msg_data['from_port']))
        print(e_error)


def get_template_file_and_save(id_template: int):
    """
    Retrieves a template file from the database, reads its contents, and saves the contents as text in the same template object.

    Args:
        id_template (int): The ID of the template file to retrieve from the database.

    Returns:
        None
    """
    template = TemplateFiles.objects.get(id=id_template)
    filename = template.file.path

    archivo = open(filename, "r")
    template.text = archivo.read()
    template.save()


def emails_cadena(cadena):
    """ Función que nos servirá para extraer todos los email válidos de una cadena de texto. """
    try:
        # Definimos una lista de signos de puntuación a eliminar, excepto @ y .
        caracteres_puntuacion = string.punctuation.replace(
            '@', '').replace('.', '')

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

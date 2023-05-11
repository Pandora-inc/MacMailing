
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import os
import string
import smtplib
from django.utils.html import format_html
from django.db import connection


def send_mail(id_mail):
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
            reportes_clientesemail.data \
        FROM \
            reportes_mail \
            INNER JOIN reportes_mailcorp ON reportes_mailcorp.id = reportes_mail.mail_corp_id \
            INNER JOIN clientes ON clientes.id = reportes_mail.cliente_id \
            INNER JOIN reportes_clientesemail ON reportes_clientesemail.cliente_id = reportes_mail.cliente_id \
        WHERE \
            reportes_mail.id = {id_mail} \
            AND reportes_clientesemail.type_id = 1"
        
        cursor.execute(consulta)
        row = cursor.fetchone()

        server = smtplib.SMTP(row[8], row[9])
        server.starttls()
        server.login(row[6], row[7])
        server.command_encoding = 'utf-8'
        # msg = "Subject: {}\n\n{}".format(row[0], row[1])

        msg = MIMEMultipart()
        msg['Subject'] = row[0]
        msg['From'] = row[5]
        msg['To'] = row[16]
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(row[1], 'html'))

        consulta_attachment = f"SELECT * FROM reportes_mail_attachment \
                                INNER JOIN reportes_attachment ON reportes_attachment.id = reportes_mail_attachment.attachment_id \
                                WHERE mail_id = {id_mail}"
        cursor.execute(consulta_attachment)
        attachment = cursor.fetchall()

        for f in attachment:
            with open('static_media/'+f[5], 'rb') as a_file:
                aux = f[5].split('.')
                basename = os.path.basename(f[4]+".%s" % aux[-1])
                part = MIMEApplication(a_file.read(), Name=basename)
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename
            msg.attach(part)


        # msg = msg.encode('utf-8', "replace")
        try:
            server.sendmail(row[5], row[16], msg.as_string())
            cursor.execute(f"UPDATE reportes_mail SET status = 1, send_number = {row[3] + 1}, last_send = NOW() WHERE id = {id_mail}")
            col_afectada = cursor.rowcount
            connection.commit()
        except Exception as e_error:
            print (e_error)
        server.quit()

def abrir_plantilla():
    pass

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
            for email in emails:
                if email[0]:
                    print(f"{email[0]}@{email[1]}")
                # de lo contrario se muestra el texto con el nombre del dominio en cuestión
                else:
                    print("No existe  un nombre de usuario en :", email[1])

    except Exception as e_error:
        print (e_error)
        print("Ha ocurrido un error inesperado al procesar la cadena.")

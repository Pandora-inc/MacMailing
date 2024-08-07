""" Módulo que contiene las API's de la aplicación de reportes """
# from .serializers import MySerializer
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError

from auxiliares.models import Country, Type
from reportes.utils import send_log_message
from reportes.constants import BITRIX_WEBHOOK, BITRIX_BASE_URL
from reportes.models import Clientes, ClientesAddress, ClientesContact, ClientesEmail, MailCorp
from reportes.serializers import ClientesSerializer

class MyAPIView(APIView):
    """ Clase que recibe un JSON y lo imprime en la consola """

    def get(self, request, *args, **kwargs):
        """ Método que imprime un mensaje en la consola """
        message = "Hola mundo"
        send_log_message(message)
        return Response({"message": message}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """ Método que recibe un JSON y lo imprime en la consola """
        id_lead = request.data.get('data[FIELDS][ID]')
        if not id_lead:
            return Response({"error": "ID lead is missing"}, status=status.HTTP_400_BAD_REQUEST)

        send_log_message(f"Received petition for lead id: {id_lead}")

        url = self.construct_url(id_lead)
        send_log_message(url)

        response = self.make_request(url)

        if response.status_code != 200:
            return Response(response.json(), status=response.status_code)

        result = response.json().get('result')
        if not result:
            return Response({"error": "Result not found"}, status=status.HTTP_400_BAD_REQUEST)

        send_log_message(f"Received data for lead id: {result['ID']} title: {result['TITLE']}")

        data = self.construct_data(result)
        if not data:
            return Response({"error": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

        return self.process_data(result, data)

    def delete(self, request, *args, **kwargs):
        """ Metodo que cambia el estado de un cliente a visible false"""
        id_lead = request.data.get('data[FIELDS][ID]')
        if not id_lead:
            return Response({"error": "ID lead is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente = Clientes.objects.get(cliente_id=id_lead)
            cliente.visible = False
            cliente.save()
            send_log_message(f"Cliente {cliente} marked as not visible")
            return Response({"message": "Cliente deleted"}, status=status.HTTP_200_OK)
        except Clientes.DoesNotExist:
            return Response({"error": "Cliente not found"}, status=status.HTTP_400_BAD_REQUEST)

    def construct_url(self, id_lead):
        """ Método que construye la URL para obtener la información de un lead """
        return f'{BITRIX_BASE_URL}/{BITRIX_WEBHOOK}/crm.lead.get.json?ID={id_lead}'

    def make_request(self, url):
        """ Método que realiza una petición POST a una URL """
        headers = {
            'Content-Type': 'html/text',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        return requests.post(url, headers=headers, timeout=5)

    def construct_data(self, result):
        """ Método que construye el diccionario de datos a partir de la información del lead """
        salutation = self.get_salutation(result['HONORIFIC'])
        lead_status = self.get_lead_status(result['STATUS_ID'])
        source = self.get_source(result['SOURCE_ID'])
        responsable = None
        if self.get_responsable(result['ASSIGNED_BY_ID']):
            responsable = self.get_responsable(result['ASSIGNED_BY_ID'])

        if result.get('UF_CRM_1644500575'):
            if Type.objects.filter(code=result['UF_CRM_1644500575']).exists() is False:
                send_log_message(f"Lead type {result['UF_CRM_1644500575']} not found")
                return None
        else:
            send_log_message(f"Lead type is empty")
            return None

        lead_type = Type.objects.get(code=result['UF_CRM_1644500575']).id

        return {
            'cliente_id': result['ID'],
            'status': lead_status,
            'lead_name': result['TITLE'],
            'salutation': salutation,
            'first_name': result['NAME'],
            'middle_name': result['SECOND_NAME'],
            'last_name': result['LAST_NAME'],
            'created': result['DATE_CREATE'],
            'source': source,
            'source_information': result['SOURCE_DESCRIPTION'],
            'modified': result['DATE_MODIFY'],
            'company_name': result['COMPANY_TITLE'],
            'position': result['POST'],
            'comment': result['COMMENTS'],
            'total': result['OPPORTUNITY'],
            'currency': 'US Dollar' if result['CURRENCY_ID'] == 'USD' else result['CURRENCY_ID'],
            'type': lead_type,
            'addl_type_details_other': result['UF_CRM_1660655104670'],
            'contacted': result['STATUS_ID'] == 'IN_PROCESS',
            'responsible': responsable.id if responsable else None,
        }

    def get_salutation(self, honorific):
        """ Método que retorna el saludo correspondiente al honorífico """
        return {
            'HNR_EN_1': 'Mr.',
            'HNR_EN_2': 'Ms.',
            'HNR_EN_3': 'Mrs.',
            'HNR_EN_4': 'Dr.'
        }.get(honorific, '')

    def get_lead_status(self, status_id):
        """ Método que retorna el estado del lead """
        return {
            'NEW': '5% Lead Find',
            'IN_PROCESS': '20% Lead Contacted',
            'PROCESSED': '35% Lead Responded',
            'UC_Z2R285': '50% Meeting / Samples / Prices',
            'UC_2KL9D9': '75% Proposal Revision Feedback',
            'UC_R0MHEU': '90% Proposal Accepted',
            'CONVERTED': '100% Client',
            'JUNK': 'On-Ice',
            'UC_CMOTYC': 'Do not contact'
        }.get(status_id, '')

    def get_source(self, source_id):
        """ Método que retorna la fuente del lead """
        return {
            'WEBFORM': 'CRM form',
            'CALLBACK': 'Callback',
            'RC_GENERATOR': 'Sales boost',
            'STORE': 'Online Store',
            'CALL': 'Call'
        }.get(source_id, '')

    def process_data(self, result, data):
        """ Método que procesa la información del lead """
        try:
            cliente = Clientes.objects.get(cliente_id=result['ID'])
            return self.update_cliente(cliente, data, result)
        except Clientes.DoesNotExist:
            return self.create_cliente(data, result)

    def update_cliente(self, cliente, data, result):
        """ Método que actualiza un cliente en la base de datos """
        serializer = ClientesSerializer(cliente, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.update_emails(cliente, result)
            self.update_phones(cliente, result)
            self.update_address(cliente, result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        send_log_message(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_cliente(self, data, result):
        """ Método que crea un cliente en la base de datos """
        serializer = ClientesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cliente = convert_to_client(result)
            self.update_emails(cliente, result)
            self.update_phones(cliente, result)
            self.update_address(cliente, result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        send_log_message(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_emails(self, cliente, result):
        """ Método que actualiza los correos electrónicos de un cliente """
        if 'EMAIL' in result:
            for email in result['EMAIL']:
                email_type = self.get_contact_type(email['VALUE_TYPE'])
                try:
                    with transaction.atomic():
                        ClientesEmail.objects.update_or_create(
                            cliente=cliente,
                            type_id=email_type,
                            defaults={'data': email['VALUE']}
                        )
                        send_log_message(f"Email {email['VALUE']} updated for cliente {cliente}")
                except IntegrityError:
                    send_log_message(
                        f"Duplicate entry found for cliente {cliente} and type_id {email_type}.")

    def update_phones(self, cliente, result):
        """ Método que actualiza los teléfonos de un cliente """
        if 'PHONE' in result:
            for phone in result['PHONE']:
                phone_type = self.get_contact_type(phone['VALUE_TYPE'])
                try:
                    with transaction.atomic():
                        ClientesContact.objects.update_or_create(
                            cliente=cliente,
                            data=phone['VALUE'],
                            type_id=phone_type
                        )
                except IntegrityError:
                    send_log_message(
                        f"Duplicate entry found for cliente {cliente} and type_id {phone_type}.")

    def update_address(self, cliente, result):
        """ Método que actualiza la dirección de un cliente """
        if result.get('ADDRESS'):
            if not result.get('ADDRESS_COUNTRY'):
                send_log_message(f"Country not found for address {result['ADDRESS']}")
            else:
                if Country.objects.filter(description=result['ADDRESS_COUNTRY']).exists():
                    country = Country.objects.get(description=result['ADDRESS_COUNTRY'])
                else:
                    country = Country.objects.create(description=result['ADDRESS_COUNTRY'])

                ClientesAddress.objects.update_or_create(
                    cliente=cliente,
                    address=result['ADDRESS'],
                    defaults={
                        'street_house_no': result.get('ADDRESS_2'),
                        'city': result.get('ADDRESS_CITY'),
                        'postal_code': result.get('ADDRESS_POSTAL_CODE'),
                        'region_area': result.get('ADDRESS_REGION'),
                        'district': result.get('ADDRESS_PROVINCE'),
                        'country_id': country
                    }
                )

    def get_contact_type(self, value_type):
        """ Método que retorna el tipo de contacto """
        return {
            'WORK': 1,
            'HOME': 2,
            'NEWSLETTER': 3
        }.get(value_type, 4)

    def get_responsable(self, responsable_id: int):
        """ Método que obtiene el responsable de un lead """
        url=f'{BITRIX_BASE_URL}/{BITRIX_WEBHOOK}/user.get.json?ID={responsable_id}'
        response = self.make_request(url)
        if response.status_code != 200:
            send_log_message(response.json())
            send_log_message(url)
            return None

        result = response.json().get('result')[0]
        if 'EMAIL' in result:
            if MailCorp.objects.filter(email=result['EMAIL']).exists():
                return MailCorp.objects.filter(email=result['EMAIL']).first()
        return None

def convert_to_client(data):
    """ Método que convierte un JSON a un objeto de tipo Clientes """
    cliente = ClientesSerializer(data=data)
    if cliente.is_valid():
        return cliente.save()
    return None

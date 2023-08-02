import openpyxl

from datetime import datetime

from auxiliares.models import ContactType, EmailType, SocialType, WebType, Country, Type
from .models import Clientes, ClientesAddress, ClientesContact, ClientesEmail, ClientesSocial, ClientesWeb, MailCorp, Account
from django.contrib.auth.models import User


''' 
Class for reading and manipulating Excel files.

Methods:
- __init__: Initializes the class with an empty workbook and active worksheet.
- open_file: Opens an Excel file and sets the workbook and active worksheet.
- clean_name: Cleans the name of a column by removing spaces, dashes, periods, commas, parentheses, and slashes.
- get_structure: Returns a dictionary with the structure of the Excel file and a dictionary with the indices.
- get_data: Returns a dictionary with the data of the Excel file and a dictionary with the indices.
- print_datos: Prints the data of the Excel file to the console and creates and saves instances of various models in a Django project based on the data.
- add_sheet: Adds a sheet to the Excel file.
- add_row: Adds a row to the active worksheet.
- save: Saves the Excel file.

Fields:
- file_name: The name of the Excel file.
- wb: The openpyxl workbook object.
- ws: The openpyxl worksheet object.
'''
class excelFile():
    ''' Clase para leer archivos excel '''
    file_name = None
    wb = None
    ws = None

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

    def open_file(self, file_name):
        ''' Abre un archivo excel '''
        self.file_name = file_name
        self.wb = openpyxl.load_workbook(file_name)
        self.ws = self.wb.active

    def clean_name(self, name):
        ''' Limpia el nombre de los campos '''
        name = str(name).lower()
        name = name.replace(" ", "_")
        name = name.replace("-", "_")
        name = name.replace(".", "")
        name = name.replace(",", "")
        name = name.replace("(", "")
        name = name.replace(")", "")
        name = name.replace("/", "")
        return name

    def get_structure(self):
        ''' Devuelve un diccionario con la estructura del excel y un diccionario con los indices '''
        response = {}
        indice = {}
        for row in self.ws.iter_rows(min_row=1, max_row=1):
            i = 0
            for cell in row:
                indice[i] = cell.value

                if cell.value:
                    indio = self.clean_name(cell.value)

                    # TODO: Este if es una excepción, hay que ver como solucionarlo
                    if i == 57:
                        indio = indio+"_dire"
                else:
                    indio = i

                response[indio] = []
                i += 1

        return response, indice

    def get_data(self) -> tuple:
        ''' Devuelve un diccionario con los datos del excel y un diccionario con los indices '''
        estructura, indice = self.get_structure()

        for row in self.ws.iter_rows(min_row=2):
            for i in range(len(row)):
                if indice[i]:
                    indio = self.clean_name(indice[i])

                    # TODO: Este if es una excepcion, hay que ver como solucionarlo
                    if i == 57:
                        indio = indio+"_dire"
                else:
                    indio = i
                dato = row[i].value
                estructura[indio].append(dato)

        return estructura, indice

    def print_datos(self):
        ''' Imprime los datos del excel '''
        data, indice = self.get_data()
        for i in range(len(data[list(data.keys())[0]])):

            if not Clientes.objects.filter(cliente_id=data['id'][i]).exists():
                cliente = Clientes()
                cliente.cliente_id = data['id'][i]
            else:
                cliente = Clientes.objects.get(cliente_id=data['id'][i])

            cliente.status = data['status'][i]
            cliente.lead_name = data['lead_name'][i]
            cliente.salutation = data['salutation'][i]
            cliente.first_name = data['first_name'][i]
            cliente.middle_name = data['middle_name'][i]
            cliente.last_name = data['last_name'][i]
            cliente.date_of_birth = data['date_of_birth'][i]
            cliente.created = datetime.strptime(
                data['created'][i], '%m/%d/%y %H:%M')
            cliente.source = data['source'][i]
            cliente.responsible = MailCorp.objects.get(
                name=data['responsible'][i])
            cliente.status_information = data['status_information'][i]
            cliente.source_information = data['source_information'][i]
            cliente.created_by = MailCorp.objects.get(
                name=data['created_by'][i])
            cliente.modified = datetime.strptime(
                data['modified'][i], '%m/%d/%y %H:%M')
            cliente.modified_by = MailCorp.objects.get(
                name=data['modified_by'][i])
            cliente.company_name = data['company_name'][i]
            cliente.position = data['position'][i]
            cliente.comment = data['comment'][i]
            cliente.total = data['total'][i]
            cliente.currency = data['currency'][i]
            cliente.product = data['product'][i]
            cliente.price = data['price'][i]
            cliente.quantity = data['quantity'][i]
            cliente.created_by_crm_form = data['created_by_crm_form'][i]
            cliente.repeat_lead = False if data['repeat_lead'][i] == 'N' else True
            cliente.client = data['client'][i]
            cliente.customer_journey = data['customer_journey'][i]
            cliente.type = Type.objects.get(
                name=data['type'][i])
            cliente.country = Country.objects.get(
                description=data['country'][i])
            cliente.account = Account.objects.get(name=data['account'][i])
            cliente.addl_type_details_other = data['addl_type_details_other'][i]
            cliente.industry_sub_type = data['industry_sub_type'][i]
            cliente.last_updated_on = datetime.strptime(
                data['last_updated_on'][i], '%m/%d/%y %H:%M')

            cliente.save()

            direccion = ClientesAddress()
            direccion.cliente = cliente
            direccion.address = data['address'][i]
            direccion.street_house_no = data['street_house_no'][i]
            direccion.apartment_office_room_floor = data['apartment_office_room_floor'][i]
            direccion.city = data['city'][i]
            direccion.district = data['district'][i]
            direccion.region_area = data['regionarea'][i]
            direccion.postal_code = data['zippostal_code'][i]
            direccion.country = data['country_dire'][i]

            direccion.save()
            cliente_id = int(cliente.cliente_id)
            e = 0
            for clave, item in data.items():
                if item[i]:

                    if indice[e] and ContactType.objects.filter(name=indice[e]):
                        if not ClientesContact.objects.filter(cliente=cliente, type=ContactType.objects.get(name=indice[e])).exists():
                            cliente.add_contact(
                                ContactType.objects.get(name=indice[e]), item[i])
                        else:
                            contact = ClientesContact.objects.get(
                                cliente=cliente, type=ContactType.objects.get(name=indice[e]))
                            contact.data = item[i]
                            contact.save()

                    elif indice[e] and WebType.objects.filter(name=indice[e]):
                        if not ClientesWeb.objects.filter(cliente=cliente, type=WebType.objects.get(name=indice[e])).exists():
                            cliente.add_web(
                                WebType.objects.get(name=indice[e]), item[i])
                        else:
                            contact = ClientesWeb.objects.get(
                                cliente=cliente, type=WebType.objects.get(name=indice[e]))
                            contact.data = item[i]
                            contact.save()

                    elif indice[e] and EmailType.objects.filter(name=indice[e]):
                        if not ClientesEmail.objects.filter(cliente=cliente, type=EmailType.objects.get(name=indice[e])).exists():
                            cliente.add_email(
                                EmailType.objects.get(name=indice[e]), item[i])
                        else:
                            contact = ClientesEmail.objects.get(
                                cliente=cliente, type=EmailType.objects.get(name=indice[e]))
                            contact.data = item[i]
                            contact.save()

                    elif indice[e] and SocialType.objects.filter(name=indice[e]):
                        if not ClientesSocial.objects.filter(cliente=cliente, type=SocialType.objects.get(name=indice[e])).exists():
                            cliente.add_social(
                                SocialType.objects.get(name=indice[e]), item[i])
                        else:
                            contact = ClientesSocial.objects.get(
                                cliente=cliente, type=SocialType.objects.get(name=indice[e]))
                            contact.data = item[i]
                            contact.save()

                e += 1

            # cliente.save()
            print("Se ha creado el cliente: ",
                  cliente.first_name, cliente.last_name)

    def add_sheet(self, sheet_name):
        ''' Agrega una hoja al archivo'''
        self.ws = self.wb.create_sheet(sheet_name)

    def add_row(self, row):
        ''' Agrega una fila al archivo '''
        self.ws.append(row)

    def save(self):
        ''' Guarda el archivo '''
        self.wb.save(self.file_name)

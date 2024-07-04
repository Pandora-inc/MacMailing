"""
    Este archivo contiene las vistas de la app reportes
"""
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render

from .forms import MailForm
from .serializers import ClientesSerializer, ExcelSerializer
from .utils import UtilExcelFile
# from reportes.serializers.excel_serializer import ClientesSerializer, ExcelSerializer

from .models import Clientes, ExcelFiles, Mail

class ClientesListAPIView(APIView):
    """ Clase que implementa la vista de la API para la lista de clientes. """
    def get(self, request):
        """ Método que se ejecuta al hacer una petición GET a la API. """
        clientes = Clientes.objects.all()
        serializer = ClientesSerializer(clientes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Método que se ejecuta al hacer una petición POST a la API. """
        serializer = ClientesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExcelsListAPIView(APIView):
    """ Clase que implementa la vista de la API para la lista de archivos Excel. """
    def get(self, request):
        """ Método que se ejecuta al hacer una petición GET a la API. """
        excels = ExcelFiles.objects.all()
        serializer = ExcelSerializer(excels, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Método que se ejecuta al hacer una petición POST a la API. """
        serializer = ExcelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProcessExcel(APIView):
    """
    This class is responsible for processing Excel files uploaded by users.
    It provides methods to read data from an Excel file and save it to the database,
    as well as retrieve data from the database and return it as a response to a POST request.
    """

    def get(self, request):
        """
        Retrieves an Excel file from the database, reads the data from the file using the
        'UtilExcelFile' class, and saves the data to the database using the 'print_datos' method
        of the 'UtilExcelFile' class.
        Returns a success response.
        """
        file = ExcelFiles.objects.get(id=2)
        excel = UtilExcelFile()
        excel.open_file(file.file.path)
        excel.print_datos()

        return Response("success")

    def post(self, request):
        """
        Retrieves data from the database using a SQL query and returns it as a response.
        """
        clientes = Clientes.objects.all()
        return Response(clientes)

def crear_correo(request):
    """ Vista para crear un nuevo correo. """
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            # Procesar el formulario y guardar el correo
            form.save()
            return render(request, 'correo_creado.html')
    else:
        print("pepinos")
        form = MailForm()

    context = {
        'form': form,  # Reemplaza my_form con tu formulario
        'opts': Mail._meta,  # Reemplaza my_model con tu modelo
        'app_label': Mail._meta.app_label,  # Nombre de la aplicación
    }
    return render(request, 'crear_correo.html', context)

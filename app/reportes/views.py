""" 
    Este archivo contiene las vistas de la app reportes
"""
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .serializers import ClientesSerializer, ExcelSerializer
from .utils import excelFile
# from reportes.serializers.excel_serializer import ClientesSerializer, ExcelSerializer

from .models import Clientes, ExcelFiles

    
class ClientesList_APIView(APIView):
    def get(self, request, format=None):
        clientes = Clientes.objects.all()
        serializer = ClientesSerializer(clientes, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ClientesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientesDetail_APIView(APIView):
    def get_object(self, pk):
        try:
            return Clientes.objects.get(pk=pk)
        except Clientes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cliente = self.get_object(pk)
        serializer = ClientesSerializer(cliente)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cliente = self.get_object(pk)
        serializer = ClientesSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cliente = self.get_object(pk)
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ExcelsList_APIView(APIView):
    def get(self, request, format=None):
        excels = ExcelFiles.objects.all()
        serializer = ExcelSerializer(excels, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
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

    def get(self, request, format=None):
        """
        Retrieves an Excel file from the database, reads the data from the file using the 'excelFile' class,
        and saves the data to the database using the 'print_datos' method of the 'excelFile' class.
        Returns a success response.
        """
        file = ExcelFiles.objects.get(id=2)
        excel = excelFile()
        excel.open_file(file.file.path)
        excel.print_datos()

        return Response("success")

    def post(self, request, format=None):
        """
        Retrieves data from the database using a SQL query and returns it as a response.
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM reportes_clientes")
        clientes = cursor.fetchall()
        return Response(clientes)
    
from rest_framework import serializers
from .models import Clientes, ExcelFiles


class ClientesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Clientes
        fields = '__all__'


class ExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFiles
        fields = '__all__'


class CompleteExcelSerializer(serializers.ModelSerializer):
     
    
    class Meta:
        model = ExcelFiles
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['clientes'] = ClientesSerializer(instance.clientes.all(), many=True).data
        return response
    
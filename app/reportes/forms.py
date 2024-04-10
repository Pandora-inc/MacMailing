from django import forms
from .models import Mail, Clientes

class MailForm(forms.ModelForm):
    """ Formulario para el envío de correos electrónicos """
    customer = forms.ModelMultipleChoiceField(queryset=Clientes.objects.all(),
                                              widget=forms.SelectMultiple)

    class Meta:
        """ Clase Meta """
        model = Mail
        fields = '__all__'
        exclude = ['cliente']
        # Campos del formulario que se mostrarán en la pantalla de administración

""" Módulo que contiene los formularios de la aplicación `reportes` """
from django import forms
from .utils import get_response_account, if_admin
from .models import Mail, Clientes

class MailForm(forms.ModelForm):
    """ Formulario para el envío de correos electrónicos """
    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        queryset = Clientes.objects.exclude(mail__isnull=False)
        if self.user and not if_admin(self.user):
            accounts = get_response_account(self.user)
            queryset = queryset.filter(responsible__in=accounts)

        ins = []

        if self.initial and 'cliente' in self.initial:
            cliente_ids = self.initial['cliente'].split(',')
            ins = Clientes.objects.filter(id__in=cliente_ids)
            self.exclude = ['cliente']

        self.fields['cliente'] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            widget=forms.SelectMultiple
        )

        self.initial['cliente'] = [cliente.id for cliente in ins]


    def save(self, commit=True):
        print("SAVE")
        instance = super().save(commit=False)

        # Verifica si el campo 'cliente' está en el formulario
        if 'cliente' in self.cleaned_data:
            cliente_instances = self.cleaned_data['cliente']
            instance.cliente.set(cliente_instances)
        else:
            raise ValueError("El campo 'cliente' debe ser una instancia de Clientes.")

        if commit:
            instance.save()

        return instance

    class Meta:
        """ Clase Meta """
        model = Mail
        fields = '__all__'

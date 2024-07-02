""" Formulario para el envío de correos electrónicos """
from django import forms

from .utils import get_response_account, if_admin
from .models import Mail, Clientes

class MailForm(forms.ModelForm):
    """ Formulario para el envío de correos electrónicos """
    user = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = Clientes.objects.exclude(mail__isnull=False)

        if self.user and not if_admin(self.user):  # Verifica si se pasó el usuario y no es admin
            accounts = get_response_account(self.user)
            queryset = queryset.filter(responsible__in=accounts)

        ins = None

        if self.initial and 'customer' in self.initial:
            ins = self.initial['customer'].split(',')

        self.fields['cliente'] = forms.ModelMultipleChoiceField(queryset=queryset,
                                              widget=forms.SelectMultiple,
                                              initial=ins)


    def save(self, commit=True):
        print("SAVE")
        instance = super().save(commit=False)

        # Verifica si el campo 'cliente' está en el formulario y es una instancia de Clientes
        if 'cliente' in self.cleaned_data and isinstance(self.cleaned_data['cliente'], Clientes):
            cliente_instance = self.cleaned_data['cliente'].first()
            instance.cliente = cliente_instance
        else:
            raise ValueError("El campo 'cliente' debe ser una instancia de Clientes.")

        if commit:
            instance.save()

        return instance

    class Meta:
        """ Clase Meta """
        model = Mail
        fields = [
            'mail_corp',
            'subject',
            'body',
            'attachment',
            'status',
            'status_response',
            'use_template',
            'template_group',
            'send_number',
            'last_send',
            'reminder_days'
        ]

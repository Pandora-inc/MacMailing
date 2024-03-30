from django import forms
from .models import Mail, Clientes

class MailForm(forms.ModelForm):
    clientes = forms.ModelMultipleChoiceField(queryset=Clientes.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Mail
        fields = ['mail_corp','clientes', 'subject', 'body']  # Campos del formulario que se mostrarán en la pantalla de administración

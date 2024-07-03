""" Archivo de configuración de la vista de administrador de Clientes """

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from reportes.models import ClientesEmail
from reportes.utils import get_response_account, if_admin


class ClientesEmailInline(admin.TabularInline):
    '''
    Tabular Inline View for ClientesEmail
    '''
    model = ClientesEmail

class ClientesAdmin(admin.ModelAdmin):
    ''' Admin View for Clientes '''
    list_display = ['cliente_id', 'last_name', 'first_name',
                    'middle_name', 'lead_name', 'status', 'responsible', 'contacted']
    search_fields = ['cliente_id', 'last_name',
                     'lead_name', 'status', 'responsible__name', 'contacted']
    ordering = ['cliente_id', 'last_name',
                'lead_name', 'status', 'responsible', 'contacted']
    list_filter = ['contacted', 'responsible', 'lead_name']
    inlines = [ClientesEmailInline]
    actions = ['enviar_mail_replicado']

    def get_queryset(self, request):
        ''' Obtener el queryset base '''
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            queryset = queryset.filter(responsible__in=accounts)

        return queryset

    def enviar_mail_replicado(self, request, queryset):
        ''' Función para crear los mails '''
        if queryset.count() > 0:

            # Redirigir al formulario de Mail replicado
            selected_clientes_ids = queryset.values_list('id', flat=True)
            additional = f'?cliente={",".join(map(str, selected_clientes_ids))}'
            url = reverse('admin:reportes_mail_add') + additional
            return redirect(url)

        mensaje = "No leads have been selected to send the replicated mail."
        self.message_user(request, message=mensaje, level='warning')
        return None

    enviar_mail_replicado.short_description = "Create a new mails"

    def save_model(self, request, obj, form, change):
        obj.save()

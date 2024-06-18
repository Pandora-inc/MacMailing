
from django.contrib import admin

from reportes.models import Clientes
from reportes.utils import get_response_account, if_admin


class ClientesEmailAdmin(admin.ModelAdmin):
    '''
    Admin View for ClientesEmail
    '''
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente__lead_name',
                     'cliente__first_name',
                     'cliente__last_name',
                     'cliente__cliente_id',
                     'type__name',
                     'data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente', 'type']

    def get_queryset(self, request):
        ''' Obtener el queryset base '''
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            clientes = Clientes.objects.filter(responsible__in=accounts)

            queryset = queryset.filter(cliente__in=clientes)

        return queryset

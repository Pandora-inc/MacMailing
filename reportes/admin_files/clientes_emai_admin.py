""" Admin de ClientesEmail """
from django.contrib import admin

from reportes.admin_files.admin_class import CommonAdminSetupMixin
from reportes.models import Clientes
from reportes.utils import get_response_account, if_admin


class ClientesEmailAdmin(CommonAdminSetupMixin, admin.ModelAdmin):
    '''
    Admin View for ClientesEmail
    '''

    def get_queryset(self, request):
        ''' Obtener el queryset base '''
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            clientes = Clientes.objects.filter(responsible__in=accounts)

            queryset = queryset.filter(cliente__in=clientes)

        return queryset

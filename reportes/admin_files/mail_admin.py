""" Admin file for Mail model """

from datetime import date
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from reportes.forms import MailForm
from reportes.utils import get_response_account, if_admin, send_log_message
from reportes.models import (Clientes, Mail, MailCorp, MailsToSend,
                             TemplateFiles, TemplatesGroup, ClientesEmail)


def prepare_to_send(_, request, queryset):
    ''' Función para preparar los emails para enviar '''
    for obj in queryset:
        if obj.status_response is False:
            if not ClientesEmail.objects.filter(cliente=obj.cliente).exists():
                messages.add_message(request,
                                     messages.ERROR, f"Client {obj.cliente} has no email.")
            else:
                mail = MailsToSend()
                mail.mail = Mail.objects.get(pk=obj.pk)
                mail.order = mail.mail.send_number
                mail.save()

                messages.add_message(request,
                                     messages.SUCCESS, f"{obj} has been added to the queue.")

prepare_to_send.short_description = "Prepare shipment"


class MailAdmin(admin.ModelAdmin):
    '''
    Admin View for Mail
    '''

    class Media:
        ''' Media files for admin '''
        js = ('admin/js/admin/admin_script.js',)

    list_display = ['mail_corp', 'cliente', 'subject', 'send_number',
                    'status', 'status_response', 'last_send', 'next']
    search_fields = ['mail_corp__name',
                     'mail_corp__email',
                     'cliente__lead_name',
                     'cliente__first_name',
                     'cliente__last_name',
                     'cliente__cliente_id',
                     'subject',
                     'send_number',
                     'status',
                     'last_send']
    ordering = ['mail_corp', 'cliente', 'subject',
                'send_number', 'status', 'last_send']
    list_filter = [('mail_corp', RelatedDropdownFilter), ('send_number', DropdownFilter),
                   'status', 'status_response']
    readonly_fields = ('body', 'subject', 'last_send', 'send_number', 'created')

    actions = [prepare_to_send]

    def get_queryset(self, request):
        # Obtener el queryset base
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            # clientes = Clientes.objects.filter(responsible__in=accounts)

            queryset = queryset.filter(mail_corp__in=accounts)

        return queryset

    def get_readonly_fields(self, request, obj=None):
        # Si 'fin' es True, establece los campos como readonly
        if obj and obj.status_response:
            return self.readonly_fields + ('mail_corp', 'cliente', 'subject', 'body',
                                           'status', 'status_response',
                                           'template_group', 'reminder_days', 'use_template',)
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Sobrescribe el campo de formulario para filtrar los clientes """
        # Define una función para filtrar los clientes basados en el campo 'responsable'
        if db_field.name == "cliente":
            if not if_admin(request.user):
                accounts = get_response_account(request.user)
                # clientes = Clientes.objects.filter(responsible__in=accounts)
                # Filtra los clientes cuyo 'responsable' coincide con un ID particular
                kwargs["queryset"] = Clientes.objects.filter(responsible__in=accounts)

        if db_field.name == 'mail_corp':
            if not if_admin(request.user):
                accounts = get_response_account(request.user)

                kwargs["queryset"] = MailCorp.objects.filter(user=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def next(self, obj):
        '''
        Calcula los días que faltan para el proximo envío
        '''
        last_send = obj.last_send
        if obj.status_response:
            return " - "

        if last_send:
            today = date.today()
            pass_days = (today - last_send.date()).days

            reminder = int(obj.reminder_days)

            dias = reminder - pass_days
            if dias >= 0:
                return dias
            return "We are late"

        return "Today is a great day"

    def get_form(self, request, obj=None, change=False, **kwargs):
        """ Sobrescribe el formulario de creación """
        # Use custom form only for creating new instances
        if obj is None:
            mail_form = MailForm
            if 'cliente' in request.GET:
                selected_clientes_ids = map(int, request.GET.get('cliente').split(','))
                initial_data = {'customer': selected_clientes_ids}
                mail_form.initial = initial_data
                mail_form.user = request.user

            kwargs['form'] = mail_form

        return super().get_form(request, obj, **kwargs)


    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """
        Handles the form submission for changing a specific form instance in the admin interface.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - object_id (str): The ID of the object being changed.
        - form_url (str): The URL of the form.
        - extra_context (dict): Any extra context data to be passed to the form.

        Behavior:
        - If the request method is POST, processes the form data.
        - Validates if the 'cliente' field is provided in the form data, displays a warning
        message if not.
        - Retrieves the 'mail_corp' ID from the form data and fetches the corresponding MailCorp
        object.
        - Validates if the 'mail_corp' is provided, displays a warning message if not.
        - Iterates over each 'cliente' ID in the form data and calls the '_handle_client_mail'
        method for each.
        - Redirects to the 'reportes_mail_changelist' URL after processing the form data.

        Returns:
        - HttpResponseRedirect: Redirects to the 'reportes_mail_changelist' URL.

        Note:
        This method is part of the MailAdmin class and is intended to be used within the Django
        admin interface for managing emails.
        """
        if request.method == 'POST':
            clientes = request.POST.getlist('cliente', None)
            if not clientes:
                self.message_user(request, "Client is required", level=messages.WARNING)
                return super().changeform_view(request, object_id, form_url, extra_context)

            mail_corp_id = request.POST.get('mail_corp', None)
            mail_corp = MailCorp.objects.filter(pk=mail_corp_id).first()
            if not mail_corp:
                self.message_user(request, "Mail Corp is required", level=messages.WARNING)
                return super().changeform_view(request, object_id, form_url, extra_context)

            for cliente_id in clientes:
                if not self._handle_client_mail(cliente_id, mail_corp, request):
                    self.message_user(request, f"{cliente_id} already have a mail.",
                                      level=messages.WARNING)

            return HttpResponseRedirect(reverse('admin:reportes_mail_changelist'))
        return super().changeform_view(request, object_id, form_url, extra_context)


    def _handle_client_mail(self, cliente_id, mail_corp, request):
        """
        Handles the creation or update of an email for a specific client and mail
        corporation.

        Parameters:
        - cliente_id (int): The ID of the client for whom the email is being handled.
        - mail_corp (MailCorp): The mail corporation associated with the email.
        - request (HttpRequest): The HTTP request object.

        Returns:
        - bool: True if the email was successfully created or updated, False otherwise.

        Behavior:
        - If no template group is provided in the request, a log message is sent and the
        method returns False.
        - Retrieves the template group based on the provided ID from the request.
        - Extracts the reminder days, status response, and status from the request data.
        - Fetches the client object based on the provided ID.
        - Checks if there is an existing email for the client and mail corporation.
            - If exists, updates the existing email with new data and saves it.
            - If not, creates a new email with the provided data and saves it.
        - If a template is found for the template group, sets the email body and subject
        accordingly.
        - Sends a success message to the user indicating the operation outcome.

        Note:
        This method is part of the MailAdmin class and is intended to be used within the Django
        admin interface for managing emails.
        """
        template_group_id = request.POST.get('template_group', None)
        if not template_group_id:
            send_log_message("NO TEMPLATE GROUP")
            return False

        template_group = TemplatesGroup.objects.filter(pk=template_group_id).first()

        reminder_days = request.POST.get('reminder_days', 7)
        status_response = request.POST.get('status_response', 'off') == 'on'
        status = request.POST.get('status', False) in ['on', 'true', 1, True, "1"]

        client = Clientes.objects.get(pk=cliente_id)

        # Buscar un correo existente para este cliente y empresa de correo
        existing_mail = Mail.objects.filter(mail_corp=mail_corp, cliente=client).first()

        if existing_mail:
            # Actualizar el correo existente
            existing_mail.status = status
            existing_mail.status_response = status_response
            existing_mail.template_group = template_group
            existing_mail.reminder_days = reminder_days
            existing_mail.save()
            self.message_user(request, f"{cliente_id} has been updated.", level=messages.SUCCESS)
            return True
        else:
            # Crear un nuevo correo si no existe uno para este cliente y empresa de correo
            mail = Mail.objects.create(
                mail_corp=mail_corp,
                cliente=client,
                status=status,
                status_response=status_response,
                template_group=template_group,
                reminder_days=reminder_days
            )

            template = TemplateFiles.objects.filter(template_group=template_group, orden=1).first()
            if template:
                mail.body = template.text
                mail.subject = template.name

            mail.save()
            self.message_user(request, f"{cliente_id} has been added.", level=messages.SUCCESS)
            return True

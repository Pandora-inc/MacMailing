""" Admin file for Mail model """

from datetime import date
from typing import Any
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from reportes.forms import MailForm
from reportes.utils import get_response_account, if_admin
from reportes.models import Clientes, Mail, MailCorp, MailsToSend, TemplateFiles, TemplatesGroup


def prepare_to_send(modeladmin, request, queryset):
    ''' Función para preparar los emails para enviar '''
    for obj in queryset:
        if obj.status_response is False:
            print(obj.status)
            mail = MailsToSend()
            mail.mail = Mail.objects.get(pk=obj.pk)
            print(obj.mail_corp)
            mail.save()

prepare_to_send.short_description = "Prepare shipment"


class MailAdmin(admin.ModelAdmin):
    '''
    Admin View for Mail
    '''

    class Media:
        ''' Media files for admin '''
        js = ('admin/js/admin/admin_script.js',)

    list_display = ['mail_corp', 'cliente', 'subject', 'send_number',
                    'status', 'status_response', 'last_send', 'proximo']
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
    list_filter = ['mail_corp', 'send_number', 'status', 'status_response']
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
                                           'attachment', 'status', 'status_response',
                                           'template_group', 'reminder_days', 'use_template',)
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Sobreescribe el campo de formulario para filtrar los clientes """
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


    def proximo(self, obj):
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
            else:
                return "Estamos atrasados"
        else:
            return "Today is a great day"

    def get_form(self, request, obj=None, **kwargs):
        """ Sobreescribe el formulario de creación """
        # Use custom form only for creating new instances
        if obj is None:

            mail_form = MailForm
            if 'customer' in request.GET:
                selected_clientes_ids = map(int, request.GET.get('customer').split(','))

                initial_data = {'customer': selected_clientes_ids}

                mail_form.initial = initial_data
                mail_form.user = request.user

            kwargs['form'] = mail_form

        return super().get_form(request, obj, **kwargs)


    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """ Sobreescribe la vista de cambio de formulario """
        # Verifica si se está guardando el formulario (si es una solicitud POST)
        if request.method == 'POST':
            clientes = request.POST.getlist('cliente', None)
            if not clientes:
                self.message_user(request, "Client is required", level=messages.WARNING)
                return super().changeform_view(request, object_id, form_url, extra_context)
            # TODO: Verificar si se puede hacer que el formulario se guarde si solo hay un cliente
            # if len(clientes) == 1:
            #     return super().changeform_view(request, object_id, form_url, extra_context)

            mail_corp_id = request.POST.get('mail_corp', None)
            mail_corp = MailCorp.objects.get(pk=mail_corp_id)
            if not mail_corp:
                self.message_user(request, "Mail Corp is required", level=messages.WARNING)
                return super().changeform_view(request, object_id, form_url, extra_context)

            template_group_id = request.POST.get('template_group', None)
            if template_group_id:
                template_group = TemplatesGroup.objects.get(pk=template_group_id)
            else:
                template_group = None

            reminder_days = request.POST.get('reminder_days', 7)

            use_template = request.POST.get('use_template', False)
            use_template = True if use_template == 'on' else False

            status_response = request.POST.get('status_response', False)
            status_response = True if status_response == 'on' else False

            status = request.POST.get('status', False)
            status = True if (status in ['on', 'true', 1, True, "1"]) else False

            for cliente in clientes:
                client = Clientes.objects.get(pk=cliente)
                if cliente:
                    if Mail.objects.filter(mail_corp=mail_corp, cliente=cliente).exists():
                        if len(clientes) == 1:
                            return super().changeform_view(request, object_id, form_url, extra_context)
                        else:
                            self.message_user(request, f"{cliente} already have a mail.", level=messages.WARNING)
                    else:
                        mail = Mail.objects.create(
                            mail_corp=mail_corp if mail_corp else None,
                            cliente=client,
                            status=status,
                            status_response=status_response,
                            use_template=use_template,
                            template_group=template_group,
                            reminder_days=reminder_days
                        )
                        if use_template and template_group:
                            template = TemplateFiles.objects.filter(template_group=template_group,
                                                                    orden=1)
                            if template.exists():
                                mail.body = template.first().text
                                mail.subject = template.first().name

                        if mail.save():
                            self.message_user(request, f"{cliente} has been added.",
                                              level=messages.SUCCESS)

            return HttpResponseRedirect(reverse('admin:reportes_mail_changelist'))
        return super().changeform_view(request, object_id, form_url, extra_context)

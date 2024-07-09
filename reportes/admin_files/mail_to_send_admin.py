""" Admin de mails a enviar """

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils import timezone
import newrelic.agent

from auxiliares.models import EmailType
from reportes.models import ClientesEmail, Mail
from reportes.utils import if_admin, get_response_account
from reportes.actions import get_mail_data, prepare_email_body, send_mail


@newrelic.agent.background_task(name='Envio de mail', group='Mail')
def enviar_email(_, request, queryset):
    """ Función para enviar email desde el admin """
    try:
        for obj in queryset:
            if obj.approved is True:
                newrelic.agent.add_custom_parameter("mail_id", obj.mail_id)
                if send_mail(obj.mail_id):
                    obj.send = True  # Marcar el correo como enviado
                    obj.save()  # Guardar el objeto actualizado en la base de datos
                    messages.success(request, f"Mail sent successfully to {obj.mail_id}")
                else:
                    messages.warning(request, f"Could not send email to {obj.mail_id}")
            else:
                messages.warning(request, f"El correo {obj.mail_id} no está aprobado")
    except KeyError as e:
        messages.error(request, f"Error sending emails. Field bad defined: {e}")
    except Exception as e:
        error_type = type(e).__name__
        messages.error(request, f"Error sending emails: {e} (Error type: {error_type})")

enviar_email.short_description = "Send email"

class MailsToSendAdmin(admin.ModelAdmin):
    '''
    Admin View for MailsToSend
    '''
    list_display = ['mail', 'approved', 'mail_to', 'mail_from']
    exclude = ('send',)
    readonly_fields = (
        'mail_from',
        'mail_subject',
        'mail_body',
        'user_approved',
        'date_approved')
    search_fields = ['mail__mail_corp__name', 'mail__cliente__lead_name',
                     'mail__cliente__last_name', 'mail__cliente__first_name', 'approved', 'send']

    ordering = ['mail', 'approved', 'send']

    def get_queryset(self, request):
        '''
        Filtra los mails que se van a enviar
        '''
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            mails = Mail.objects.filter(mail_corp__in=accounts)
            queryset = queryset.filter(mail__in=mails, send=False)
        else:
            queryset = queryset.filter(send=False)

        return queryset

    def mail_body(self, obj):
        '''
        Muestra el cuerpo del mail
        '''

        body = obj.mail.body if obj.mail.body else ''
        firma = obj.mail.mail_corp.firma if obj.mail.mail_corp.firma else ''
        body += '<br>' + firma
        msg_data = get_mail_data(obj.mail.id)
        body = prepare_email_body(body, msg_data)

        return mark_safe(body)

    def mail_subject(self, obj):
        '''
        Muestra el asunto del mail
        '''
        return obj.mail.subject

    def mail_from(self, obj):
        '''
        Muestra el mail del remitente
        '''
        return obj.mail.mail_corp.email

    def mail_to(self, obj):
        '''
        Muestra el mail del destinatario

        Parameters:
            obj: Object
                The object containing the mail information.

        Returns:
            str
                The email address of the recipient.

        Raises:
            ClientesEmail.DoesNotExist
                If the recipient email does not exist in the database.

        '''
        try:
            email = ClientesEmail.objects.get(
                cliente=obj.mail.cliente, type=EmailType.objects.get(id=1))
            return email.data
        except ClientesEmail.DoesNotExist:
            email = ClientesEmail.objects.get(cliente=obj.mail.cliente).first()
            return email.data


    def save_model(self, request, obj, form, change):
        # Verifica si el campo 'approved' cambió a True y 'user_approved' aún no está establecido
        if obj.approved and not obj.user_approved:
            # Asigna el usuario actual
            obj.user_approved = request.user
            # Asigna la fecha y hora actual
            obj.date_approved = timezone.now()
        super().save_model(request, obj, form, change)

    mail_body.short_description = 'Email Body'
    mail_subject.short_description = 'Email subject'

    actions = [enviar_email]

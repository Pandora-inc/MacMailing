""" Admin de la app reportes """
from django.contrib import admin

from .admin_files import clientes_emai_admin
from .admin_files.admin_class import (AccountAdmin, AttachmentAdmin, ClientesAddressAdmin,
                          ClientesContactAdmin, ClientesSocialAdmin, ClientesUTMAdmin,
                          ClientesWebAdmin, ExcelFilesAdmin, MailCorpAdmin,
                          TemplateFilesAdmin, TemplateGroupAdmin)
from .admin_files.mail_admin import MailAdmin
from .admin_files.clientes_admin import ClientesAdmin
from .admin_files.mail_to_send_admin import MailsToSendAdmin
from .models import (Account, Attachment, Clientes, ClientesAddress, ClientesContact,
                     ClientesEmail, ClientesSocial, ClientesUTM, ClientesWeb, ExcelFiles,
                     Mail, MailCorp, MailsToSend, TemplateFiles, TemplatesGroup)

admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(ClientesAddress, ClientesAddressAdmin)
admin.site.register(ClientesContact, ClientesContactAdmin)
admin.site.register(ClientesEmail, clientes_emai_admin.ClientesEmailAdmin)
admin.site.register(ClientesSocial, ClientesSocialAdmin)
admin.site.register(ClientesUTM, ClientesUTMAdmin)
admin.site.register(ClientesWeb, ClientesWebAdmin)
admin.site.register(ExcelFiles, ExcelFilesAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(MailsToSend, MailsToSendAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(MailCorp, MailCorpAdmin)
admin.site.register(TemplatesGroup, TemplateGroupAdmin)
admin.site.register(TemplateFiles, TemplateFilesAdmin)

admin.site.site_header = 'MacMailing'

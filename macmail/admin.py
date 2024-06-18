from django.contrib import admin

admin.site.site_header = 'Mi sitio web de Django'
admin.site.site_title = 'Mi sitio web de Django'

class MiAdminSite(admin.AdminSite):
    site_header = 'Mi sitio web de Django'
    site_title = 'Mi sitio web de Django'
    index_title = 'Bienvenido al panel de administración de Mi sitio web de Django'

admin_site = MiAdminSite()
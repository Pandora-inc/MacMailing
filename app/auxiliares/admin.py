''' Configuraciones particulares para el panel de administración '''
from django.contrib import admin
from app.auxiliares.models import ContactType, Country, EmailType, SocialType, Type, WebType


class TypeAdmin(admin.ModelAdmin):
    ''' Configuraciones particulares para el modelo Type '''
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name', 'description']

class ContactTypeAdmin(admin.ModelAdmin):
    ''' Configuraciones particulares para el modelo ContactType '''
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name', 'description']

class CountryAdmin(admin.ModelAdmin):
    ''' Configuraciones particulares para el modelo Country '''
    list_display = ['description']
    search_fields = ['description']
    ordering = ['description']

class EmailTypeAdmin(admin.ModelAdmin):
    ''' Configuraciones particulares para el modelo EmailType '''
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name', 'description']

class SocialTypeAdmin(admin.ModelAdmin):
    ''' Configuraciones particulares para el modelo SocialType '''
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name', 'description']

class WebTypeAdmin(admin.ModelAdmin):
    ''' Configuraciones particulares para el modelo WebType '''
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name', 'description']


admin.site.register(Type, TypeAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ContactType, ContactTypeAdmin)
admin.site.register(WebType, WebTypeAdmin)
admin.site.register(EmailType, EmailTypeAdmin)
admin.site.register(SocialType, SocialTypeAdmin)

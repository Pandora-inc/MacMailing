""" Configuraciones del Admin """
from django import forms
from django.utils.html import format_html
from django.contrib import admin
from reportes.models import LibrosRubricados, RegistrosLibros



class LibrosAdmin(admin.ModelAdmin):
    change_form_template = 'admin/new_change_form.html'
    # añade un campo de texto para realizar la búsqueda, puedes añadir mas de un atributo
    search_fields = ['fecha', 'tipo', 'impresion']
    # añade una lista desplegable con la que podrás filtrar (activo es un atributo booleano)
    list_filter = ['status']
    fieldsets = (
        (id, {
            'fields': ('nombre',)
        }),
        (' ', {
            'fields': ('tipo', 'impresion')
        }),
        ('*', {
            'fields': ('fecha_desde', 'fecha_hasta', 'pagina_desde', 'pagina_hasta')
        }),
        (None, {
            'fields': ('button_generar', 'button_imprimir')
        })
    )
    readonly_fields = ('button_generar', 'button_imprimir')

    def button_imprimir(self, request):
        print("Aca se imprime en pdf")
    
    def button_generar(self, request):
        # return get_button("actividad", "polizas", request.nombre, "Polizas cliente")
        return format_html('<input type="submit" value="Guardar y continuar editando" name="_continue">')

class RegistrosLibrosAdmin(admin.ModelAdmin):
    change_form_template = 'admin/new_change_form.html'
    search_fields = ['libro', 'numero', 'fecha']
    list_filter = ['libro']

admin.site.register(LibrosRubricados, LibrosAdmin)
admin.site.register(RegistrosLibros, RegistrosLibrosAdmin)

""" Modelo de datos relacionados a la actividad """
from django.db import models


TIPOS_LIBROS = [
    ('Operaciones', 'Operaciones'),
    ('Rendiciones', 'Rendiciones'),
]

TIPOS_IMPRESION = [
    ('Encabezados', 'Imprimir Encabezados'),
    ('Rubricados', 'Imprimir Rubricados'),
]

class LibrosRubricados(models.Model):
    """ Modelo para la generación de libros de rendiciones y operaciones """
    nombre = models.CharField(max_length=32)
    fecha = models.DateField(blank=True, null=True, verbose_name='Fecha',
                             help_text='Fecha de la operación', auto_now_add=True)
    impresion = models.CharField(
        max_length=16, choices=TIPOS_IMPRESION, verbose_name='Impresión',blank=True, null=True, )
    tipo = models.CharField(
        max_length=16, choices=TIPOS_LIBROS, verbose_name='Tipo')
    status = models.BooleanField(default=True, verbose_name='Activo')
    fecha_desde = models.DateField(blank=True, null=True)
    fecha_hasta = models.DateField(blank=True, null=True)
    pagina_desde = models.IntegerField(blank=True, null=True)
    pagina_hasta = models.IntegerField(blank=True, null=True)
    generado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " - " + str(self.nombre)

    class Meta:
        """ Meta """
        # managed = False
        db_table = 'libro_rubricados'
        verbose_name = 'libro rubricado'
        verbose_name_plural = 'libros rubricados'
        ordering = ('fecha',)


class RegistrosLibros(models.Model):
    """ Modelo para el registro de los items de los libros de rendiciones y operaciones """
    libro = models.ForeignKey(
        LibrosRubricados, models.RESTRICT, blank=True, null=True)
    numero = models.IntegerField(
        blank=True, null=True, verbose_name='Numero de orden')
    fecha = models.DateField(blank=True, null=True,
                             help_text='Fecha de registro de la poliza')
    vigencia_desde = models.DateField(
        blank=True, null=True, help_text='Fecha de la vigencia desde de la poliza')
    vigencia_hasta = models.DateField(
        blank=True, null=True, help_text='Fecha de la vigencia hasta de la poliza')
    prima = models.DecimalField(
        max_digits=11, decimal_places=2, help_text='Prima de la poliza')
    cliente_nombre = models.CharField(
        max_length=64, help_text='Nombre registrado del cliente')
    cliente_direccion = models.CharField(
        max_length=64, help_text='Direccion del cliente')
    compania_nombre = models.CharField(
        max_length=32, help_text='Nombre de la compañia')
    orden_direccion = models.CharField(
        max_length=64, help_text='Direccion registrada de la orden. Ubicacion del riesgo')
    riesgo_desc = models.TextField(help_text='Descripcion del riesgo de la orden. Bien a asegurar')
    secciones = models.CharField(
        max_length=64, help_text='Nombre de la seccion de la orden. Riesgo a cubrir')
    observaciones = models.CharField(max_length=64)

    def __str__(self):
        return str(self.libro) + " - " + str(self.numero) + " - " + str(self.cliente_nombre)

    class Meta:
        """ Meta data del modelo """
        # managed = False
        db_table = 'registros_libros'
        verbose_name = 'registro libro'
        verbose_name_plural = 'registros libros'
        ordering = ('libro', 'fecha')

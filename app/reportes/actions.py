
from django.utils.html import format_html
from django.db import connection

from reportes.models import LibrosRubricados, RegistrosLibros


def colect_libro(cosas):
    id_libro = 2
    # print(cosas)
    with connection.cursor() as cursor:
        libro = LibrosRubricados.objects.get(id=id_libro)
        sql = "SELECT ordenes.numero, polizas.fecha, polizas.vigencia_desde, polizas.vigencia_hasta, polizas.prima, clientes.nombre, clientes.direccion, companias.nombre, ordenes.direccion, ordenes.riesgo_desc, secciones.nombre, 'observaciones' FROM polizas, ordenes, clientes, companias, secciones WHERE polizas.fecha BETWEEN '" + \
            str(libro.fecha_desde)+"' AND '"+str(libro.fecha_hasta) + \
            "' AND polizas.id = ordenes.poliza_id AND polizas.cliente_id = clientes.id AND polizas.compania_id = companias.id AND polizas.seccion_id = secciones.id ORDER BY polizas.fecha"

        cursor.execute(sql)
        ordenes = cursor.fetchall()

        for orden in ordenes:
            if not RegistrosLibros.objects.get(numero=orden[0], libro=libro):
                registro = RegistrosLibros(
                    libro=libro,
                    numero=orden[0],
                    fecha=orden[1],
                    vigencia_desde=orden[2],
                    vigencia_hasta=orden[3],
                    prima=orden[4],
                    cliente_nombre=orden[5],
                    cliente_direccion=orden[6],
                    compania_nombre=orden[7],
                    orden_direccion=orden[8],
                    riesgo_desc=orden[9],
                    secciones=orden[10],
                    observaciones=orden[11]
                )

            registro.save()

        return True

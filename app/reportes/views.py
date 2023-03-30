from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator
from django.utils import timezone
from django.db import connection

from .forms import ClientesPolizasForm, CompaniaForm, LibrosRubricadosForm, VencimientoPolizasForm
from .models import Clientes, Companias, Secciones, Productores, Ordenes, Polizas


# Create your views here.

def libros_rubricados(request, libro_id):
    """Libros rubricados"""
    if request.method == "POST":
        form = LibrosRubricadosForm(request.POST)

        if form.is_valid():

            if int(request.POST.get('encRubr')) == 2:
                if int(request.POST.get('rendOp')) == 1:
                    ordenes = recuperar_rubri_rendiciones(request.POST.get(
                        'vigencia_desde'), request.POST.get('vigencia_hasta'))
                else:
                    ordenes = recuperar_rubri_operaciones(request.POST.get(
                        'vigencia_desde'), request.POST.get('vigencia_hasta'))
                    

            return render(request, 'libros_rubricados.html', {'ordenes': ordenes})
    else:
        form = LibrosRubricadosForm()
        return render(request, 'form_libros.html', {'form': form})

def recuperar_rubri_operaciones(fecha_desde, fecha_hasta):
    with connection.cursor() as cursor:
        print(fecha_desde, fecha_hasta)
        sql = "SELECT ordenes.numero, polizas.fecha, polizas.vigencia_desde, polizas.vigencia_hasta, polizas.prima, clientes.nombre, clientes.direccion, companias.nombre, ordenes.direccion, ordenes.riesgo_desc, secciones.nombre, 'observaciones' FROM     polizas, ordenes, clientes, companias, secciones WHERE polizas.fecha BETWEEN '"+fecha_desde+"' AND '"+fecha_hasta+"' AND polizas.id = ordenes.poliza_id AND polizas.cliente_id = clientes.id AND polizas.compania_id = companias.id AND polizas.seccion_id = secciones.id ORDER BY polizas.fecha"
        print (sql)
        cursor.execute(sql)
        ordenes = cursor.fetchall()
        return ordenes

def recuperar_rubri_rendiciones(fecha_desde, fecha_hasta):
    with connection.cursor() as cursor:
        sql = "SELECT 1, pagos_cuotas.fecha, polizas.numero, companias.nombre, pagos_cuotas.importe, 0, cuotas_polizas.nro_cuota, polizas.cant_cuotas FROM polizas, companias, cuotas_polizas, pagos_cuotas WHERE polizas.id = cuotas_polizas.poliza_id AND cuotas_polizas.id = pagos_cuotas.cuota_id AND polizas.compania_id = companias.id AND pagos_cuotas.fecha BETWEEN '%s' AND '%s' UNION SELECT 2, rendiciones.fecha, polizas.numero, companias.nombre, 0, SUM(pagos_cuotas.importe), cuotas_polizas.nro_cuota, polizas.cant_cuotas FROM rendiciones, polizas, companias, pagos_cuotas, cuotas_polizas WHERE rendiciones.cuota_id = cuotas_polizas.id AND rendiciones.poliza_id = polizas.id AND polizas.id = cuotas_polizas.poliza_id AND cuotas_polizas.id = pagos_cuotas.cuota_id AND polizas.compania_id = companias.id AND rendiciones.fecha BETWEEN '%s' AND '%s' ORDER BY 2"

        cursor.execute(sql, (
            fecha_desde,
            fecha_hasta,
            fecha_desde,
            fecha_hasta))
        
        row = cursor.fetchall()
    return row
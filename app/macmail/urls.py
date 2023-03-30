"""macmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path #, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from actividad import views as views_actividad
from reportes import actions
# from modeladmin_reorder import reorder
# from reportes import admin as admin_reportes

urlpatterns = [
    # re_path(r'^admin/polizas/reporte/$', polizas.admin_views.vencimiento_polizas, name='reporte'),
    path('admin/', admin.site.urls),
    # path('myadmin/', admin_reportes.my_admin_site.urls),
    # path('admin/reorder/', reorder),
    # re_path(r'^actividad/clientes/$', views_actividad.ClientesListView.as_view(), name='clientes'),
    # re_path(r'^actividad/polizas/reporte/vto/$', views_actividad.vencimiento_polizas),
    # re_path(r'^actividad/polizas/reporte/cliente/$', views_actividad.cliente_polizas),
    # re_path(r'^actividad/polizas/reporte/libros/$', views_actividad.libros_rubricados),
    # re_path(r'^actividad/polizas/reporte/libros_2/$', actions.colect_libro),
    # re_path(r'^actividad/$', include('actividad.urls')),
    re_path(r'^$', TemplateView.as_view(template_name='static_pages/index.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
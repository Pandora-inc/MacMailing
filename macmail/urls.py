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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from calendarapp.views.other_views import CalendarViewIndex
from reportes.views import ClientesListAPIView, ExcelsListAPIView, ProcessExcel, crear_correo
from reportes.actions import EmailAPI, send_mail_api
import reportes.timer_to_send_email as timer_to_send

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('admin/', admin.site.urls),
    path("admin/", CalendarViewIndex.as_view(), name="calendar"),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('clientes/', ClientesListAPIView.as_view(), name='clientes'),
    path('excels/', ExcelsListAPIView.as_view(), name='archivos'),
    path('excels_work/', ProcessExcel.as_view(), name='excels_work'),
    path("", include("calendarapp.urls")),
    path("send_email/<int:id_mail>", send_mail_api, name="send_email"),
    path("send_next_email/", EmailAPI.send_next_mail, name="send_next_email"),
    path("timer_to_send_email/", timer_to_send.timer_to_send_email, name="timer_to_send_email"),
    path('muchos_correos/', crear_correo, name='crear_correo'),
    path('', include('reportes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# core/urls.py (ou o nome do seu diretório principal)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('firedata/', include('firedata.urls')),  # Inclui as URLs da sua aplicação firedata
]

# firedata/urls.py
from django.urls import path
from .views import processar_csv_e_inserir_dados

urlpatterns = [
    path('inserir-dados/', processar_csv_e_inserir_dados, name='inserir-dados'),
]

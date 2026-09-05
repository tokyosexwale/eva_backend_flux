from django.urls import path
from . import views

app_name = 'principal'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('directores/', views.lista_directores, name='directores'),
]
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('peliculas/', views.lista_peliculas, name='lista_peliculas'),
    path('pelicula/<slug:slug>/', views.detalle_pelicula, name='detalle_pelicula'),
]
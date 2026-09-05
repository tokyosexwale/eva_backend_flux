import json
import os
from django.shortcuts import render, Http404
from django.conf import settings

def obtener_lista_peliculas(ruta_json):
    """Función auxiliar para cargar las películas soportando ambos formatos de JSON."""
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    
    # Si el JSON es un diccionario con la clave 'data', extrae la lista.
    # Si ya es una lista directa, la usa tal cual.
    if isinstance(datos, dict):
        return datos.get('data', [])
    elif isinstance(datos, list):
        return datos
    return []

# Vista 1: Catálogo de Películas
def lista_peliculas(request):
    ruta_json = os.path.join(settings.BASE_DIR, 'data', 'movies.json')
    peliculas = obtener_lista_peliculas(ruta_json)
        
    busqueda_query = request.GET.get('q', None)
    
    if busqueda_query:
        busqueda_lower = busqueda_query.lower()
        peliculas = [
            peli for peli in peliculas
            if isinstance(peli, dict) and (
                busqueda_lower in peli.get('title', '').lower()
                or busqueda_lower in peli.get('synopsis', '').lower()
                or any(busqueda_lower in cat.lower() for cat in peli.get('categories', []))
            )
        ]
        
    contexto = {
        'peliculas': peliculas,
        'busqueda': busqueda_query or ''
    }
    return render(request, 'catalogo/peliculas.html', contexto)

# Vista 2: Detalle individual de la película por Slug
def detalle_pelicula(request, slug):
    ruta_json = os.path.join(settings.BASE_DIR, 'data', 'movies.json')
    peliculas = obtener_lista_peliculas(ruta_json)
        
    pelicula_encontrada = next(
        (p for p in peliculas if isinstance(p, dict) and p.get('slug') == slug), 
        None
    )
    
    if not pelicula_encontrada:
        raise Http404("La película no existe")
    
    contexto = {
        'pelicula': pelicula_encontrada
    }
    return render(request, 'catalogo/detalle.html', contexto)
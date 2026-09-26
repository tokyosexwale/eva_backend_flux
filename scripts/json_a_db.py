import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flux.settings')
django.setup()

from principal.models import Director
from catalogo.models import Pelicula, Categoria

def cargar_datos():
    # 1. Cargar Directores
    with open('data/directores.json', 'r', encoding='utf-8') as f:
        directores_data = json.load(f)
        if isinstance(directores_data, dict):
            directores_data = directores_data.get('data', [])

    for d in directores_data:
        Director.objects.get_or_create(
            id_director=d.get('id', f"dir-{d['nombre']}"),
            defaults={
                'nombre': d.get('nombre'),
                'pais': d.get('pais', 'Desconocido'),
                'estilo': d.get('estilo', 'Cine de Culto'),
                'obra_destacada': d.get('obra_destacada', ''),
                'bio': d.get('bio', '')
            }
        )

    # 2. Cargar Películas
    with open('data/movies.json', 'r', encoding='utf-8') as f:
        movies_data = json.load(f)
        if isinstance(movies_data, dict):
            movies_data = movies_data.get('data', [])

    for m in movies_data:
        # Buscar o crear director principal
        nombre_dir = m.get('director', '').split(',')[0].strip()
        director_obj = Director.objects.filter(nombre__icontains=nombre_dir).first()
        if not director_obj:
            director_obj = Director.objects.create(
                id_director=f"dir-auto-{m['slug']}",
                nombre=nombre_dir or "Director Desconocido",
                pais=m.get('country', 'Internacional'),
                estilo="Cine de Culto",
                bio="Registro creado automáticamente."
            )

        meta = m.get('metadata', {})
        images = m.get('images', {})

        peli, _ = Pelicula.objects.get_or_create(
            id_pelicula=m.get('id', f"film-{m['slug']}"),
            defaults={
                'slug': m.get('slug'),
                'title': m.get('title'),
                'year': m.get('year', 2000),
                'director': director_obj,
                'country': m.get('country', ''),
                'runtime_minutes': m.get('runtime_minutes', 0),
                'synopsis': m.get('synopsis', ''),
                'poster_url': images.get('poster', ''),
                'cult_status': meta.get('cult_status', 'Película de culto'),
                'format_type': meta.get('format', 'Digital'),
                'audio': meta.get('audio', 'Estéreo'),
            }
        )

        # Categorías
        for cat_name in m.get('categories', []):
            cat_obj, _ = Categoria.objects.get_or_create(nombre=cat_name.strip())
            peli.categorias.add(cat_obj)

    print("¡Migración de JSON a Base de Datos completada con éxito!")

if __name__ == '__main__':
    cargar_datos()
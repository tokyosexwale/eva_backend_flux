from django.shortcuts import render, get_object_or_404
from .models import Pelicula

def lista_peliculas(request):
    query = request.GET.get('q', '')
    if query:
        peliculas = Pelicula.objects.filter(
            title__icontains=query
        ) | Pelicula.objects.filter(
            synopsis__icontains=query
        )
    else:
        peliculas = Pelicula.objects.all()

    return render(request, 'catalogo/peliculas.html', {'peliculas': peliculas, 'query': query})

def detalle_pelicula(request, slug):
    pelicula = get_object_or_404(Pelicula, slug=slug)
    return render(request, 'catalogo/detalle.html', {'pelicula': pelicula})
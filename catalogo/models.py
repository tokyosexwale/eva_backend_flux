from django.db import models
from principal.models import Director  # Relación con ForeignKey

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    id_pelicula = models.CharField(max_length=20, primary_key=True)  # ej: film-001
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    year = models.IntegerField(verbose_name="Año")
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="peliculas")
    country = models.CharField(max_length=100, verbose_name="País")
    runtime_minutes = models.IntegerField(verbose_name="Duración (min)")
    synopsis = models.TextField(verbose_name="Sinopsis")
    poster_url = models.URLField(max_length=500, verbose_name="URL del Póster")
    
    # Metadatos
    cult_status = models.TextField(verbose_name="Estatus de Culto")
    format_type = models.CharField(max_length=50, verbose_name="Formato (35mm/16mm/etc)")
    audio = models.CharField(max_length=100, verbose_name="Audio")
    
    categorias = models.ManyToManyField(Categoria, related_name="peliculas")

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"

    def __str__(self):
        return f"{self.title} ({self.year})"
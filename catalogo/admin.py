from django.contrib import admin
from .models import Pelicula, Categoria

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director', 'country', 'format_type')
    search_fields = ('title', 'synopsis', 'director__nombre')
    list_filter = ('year', 'format_type', 'categorias')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
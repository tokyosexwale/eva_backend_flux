import json
import os
from django.shortcuts import render
from django.conf import settings

# Vista 1: Presentación / Inicio
def inicio(request):
    return render(request, 'principal/inicio.html')

# Vista 2: Lectura del primer JSON (Directores)
def lista_directores(request):
    ruta_json = os.path.join(settings.BASE_DIR, 'data', 'directores.json')
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        directores = json.load(archivo)
        
    contexto = {
        'directores': directores
    }
    return render(request, 'principal/directores.html', contexto)
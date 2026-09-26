# -*- coding: utf-8 -*-
import json
import os

# Definición de reglas específicas para películas emblemáticas
METADATOS_ESPECIFICOS = {
    "eraserhead-1977": {
        "cult_status": "Obra cumbre del cine de medianoche y vanguardia industrial",
        "format": "35mm B&N",
        "audio": "Mono / Sonido Industrial"
    },
    "el-topo-1970": {
        "cult_status": "Piedra angular del movimiento Midnight Movie y el Western psicodélico",
        "format": "35mm color",
        "audio": "Español Mono"
    },
    "meshes-of-the-afternoon-1943": {
        "cult_status": "Canon fundacional del cine experimental estadounidense",
        "format": "16mm B&N",
        "audio": "Sin diálogo / Música de cámara"
    },
    "pink-flamingos-1972": {
        "cult_status": "Ícono supremo del cine trash y la cultura camp",
        "format": "16mm color",
        "audio": "Mono"
    },
    "begotten-1990": {
        "cult_status": "Mito del cine experimental y el horror alegórico impreso foto a foto",
        "format": "16mm B&N procesado",
        "audio": "Efectos sonoros / Sin diálogo"
    },
    "the-room-2003": {
        "cult_status": "Fenómeno global del cine 'So Bad It's Good'",
        "format": "35mm / HD 1080p",
        "audio": "Estéreo"
    }
}

def autocompletar_metadata(pelicula):
    slug = pelicula.get('slug', '')
    meta = pelicula.get('metadata', {})
    year = pelicula.get('year', 2000)
    cats = [c.lower() for c in pelicula.get('categories', [])]

    # Si la película tiene metadatos específicos definidos, usarlos
    if slug in METADATOS_ESPECIFICOS:
        return METADATOS_ESPECIFICOS[slug]

    # Asignación de formato predeterminado según año o categoría
    if not meta.get('format'):
        if "avant-garde" in cats or "underground" in cats:
            meta['format'] = "16mm B&N" if year < 1980 else "16mm color"
        elif year < 1995:
            meta['format'] = "35mm color"
        elif year < 2005:
            meta['format'] = "35mm / Digital"
        else:
            meta['format'] = "Digital"

    # Asignación de estado de culto predeterminado si está vacío
    if not meta.get('cult_status'):
        if "horror" in cats or "splatter" in cats:
            meta['cult_status'] = "Clásico de culto del cine de género y horror"
        elif "avant-garde" in cats:
            meta['cult_status'] = "Referencia clave del cine experimental y de vanguardia"
        else:
            meta['cult_status'] = "Título de culto en el circuito de proyección independiente"

    # Preservar o formatear el audio
    if not meta.get('audio'):
        meta['audio'] = "Estéreo" if year >= 1985 else "Mono"

    return meta

def main():
    ruta_json = os.path.join('data', 'movies.json')
    if not os.path.exists(ruta_json):
        ruta_json = 'peliculas.json'

    with open(ruta_json, 'r', encoding='utf-8') as f:
        contenido = json.load(f)

    # Detectar la estructura (lista directa o diccionario con clave 'data')
    if isinstance(contenido, dict):
        peliculas = contenido.get('data', [])
    else:
        peliculas = contenido

    modificados = 0
    for peli in peliculas:
        peli['metadata'] = autocompletar_metadata(peli)
        modificados += 1

    # Guardar de vuelta en el archivo original
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(contenido, f, ensure_ascii=False, indent=2)

    print(f"Se actualizaron los metadatos de {modificados} películas en '{ruta_json}'.")

if __name__ == "__main__":
    main()
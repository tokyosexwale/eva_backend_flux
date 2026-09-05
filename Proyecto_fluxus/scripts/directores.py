# -*- coding: utf-8 -*-
import json
import os

def cargar_json(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    if isinstance(datos, dict):
        return datos.get('data', [])
    return datos

def main():
    ruta_movies = os.path.join('data', 'movies.json')
    ruta_directores = os.path.join('data', 'directores.json')

    if not os.path.exists(ruta_movies):
        ruta_movies = 'peliculas.json'

    movies = cargar_json(ruta_movies)
    directores = cargar_json(ruta_directores)

    # Crear conjunto de nombres de directores existentes
    directores_existentes = {d.get('nombre') for d in directores if isinstance(d, dict)}
    
    # Identificar directores presentes en películas pero no registrados en directores.json
    directores_faltantes = set()
    total_peliculas = len(movies)

    for peli in movies:
        if isinstance(peli, dict):
            dir_name = peli.get('director')
            if dir_name:
                # Si hay varios directores separados por coma, evaluar cada uno
                nombres = [n.strip() for n in dir_name.split(',')]
                for n in nombres:
                    if n and n not in directores_existentes:
                        directores_faltantes.add(n)

    print(f"Resumen de Validación:")
    print(f" - Total Películas: {total_peliculas}")
    print(f" - Directores Registrados: {len(directores_existentes)}")
    print(f" - Directores Faltantes: {len(directores_faltantes)}")

    # Si hay directores faltantes, agregarlos automáticamente con una plantilla base
    if directores_faltantes:
        print("\n⚙️ Agregando directores faltantes a directores.json...")
        next_id = len(directores) + 1
        
        for nombre in sorted(directores_faltantes):
            nuevo_director = {
                "id": f"dir-{next_id:03d}",
                "nombre": nombre,
                "pais": "Internacional",
                "estilo": "Cine de Culto / Autor",
                "obra_destacada": "",
                "bio": f"Director y realizador cinematográfico."
            }
            directores.append(nuevo_director)
            next_id += 1

        # Guardar lista actualizada de directores
        with open(ruta_directores, 'w', encoding='utf-8') as f:
            json.dump(directores, f, ensure_ascii=False, indent=2)

        print(f"Se agregaron {len(directores_faltantes)} directores nuevos a '{ruta_directores}'.")
    else:
        print("\n✨ ¡Todos los directores están correctamente registrados y sincronizados!")

if __name__ == "__main__":
    main()
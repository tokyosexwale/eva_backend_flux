# -*- coding: utf-8 -*-
"""
build_movies_json.py

Genera peliculas.json con 150 títulos curados consultando la API de TMDB.
"""

import os
import re
import json
import time
import requests

API_KEY = os.environ.get("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"

CURATED_TITLES = [
    # Avant-Garde / Cine Estructural / Underground Queer
    ("Eraserhead", 1977),
    ("El Topo", 1970),
    ("Meshes of the Afternoon", 1943),
    ("Scorpio Rising", 1963),
    ("Flaming Creatures", 1963),
    ("Chelsea Girls", 1966),
    ("Wavelength", 1967),
    ("Empire", 1964),
    ("A Movie", 1958),
    ("Fireworks", 1947),
    ("Pink Narcissus", 1971),

    # Trash / Camp / Exploitation / Midnight Movies
    ("Pink Flamingos", 1972),
    ("Female Trouble", 1974),
    ("Desperate Living", 1977),
    ("Multiple Maniacs", 1970),
    ("Faster, Pussycat! Kill! Kill!", 1965),
    ("Reefer Madness", 1936),
    ("Freaks", 1932),
    ("Mondo Cane", 1962),
    ("Blood Feast", 1963),
    ("Forbidden Zone", 1980),
    ("The Rocky Horror Picture Show", 1975),
    ("The Room", 2003),

    # Body Horror / Cyberpunk / Cine B
    ("Videodrome", 1983),
    ("Society", 1989),
    ("Basket Case", 1982),
    ("Frankenhooker", 1990),
    ("The Toxic Avenger", 1984),
    ("Tromeo and Juliet", 1996),
    ("Class of Nuke 'Em High", 1986),
    ("Repo Man", 1984),
    ("Tetsuo: The Iron Man", 1989),
    ("Tetsuo II: Body Hammer", 1992),

    # Splatter / Gore / Shockumentary
    ("Braindead", 1992),
    ("Bad Taste", 1987),
    ("Faces of Death", 1978),
    ("Tokyo Gore Police", 2008),
    ("Guinea Pig 2: Flowers of Flesh and Blood", 1985),
    ("Nekromantik", 1987),
    ("Nekromantik 2", 1991),

    # Novo Extremismo Francés / Horror de Autor
    ("À l'intérieur", 2007),
    ("Haute Tension", 2003),
    ("Frontière(s)", 2007),
    ("Irréversible", 2002),
    ("Enter the Void", 2009),
    ("Antichrist", 2009),
    ("Martyrs", 2008),

    # Cine Extremo Asiático (Japón / Corea / Hong Kong)
    ("Audition", 1999),
    ("Ichi the Killer", 2001),
    ("In the Realm of the Senses", 1976),
    ("Wild Zero", 1999),
    ("Oldboy", 2003),
    ("Battle Royale", 2000),
    ("Suicide Club", 2001),
    ("Tetsuo", 1989),
    ("Ebola Syndrome", 1996),
    ("The Untold Story", 1993),

    # Giallo / Gore Italiano
    ("Suspiria", 1977),
    ("Zombi 2", 1979),
    ("The Beyond", 1981),
    ("Deep Red", 1975),
    ("Tenebre", 1982),
    ("Cannibal Holocaust", 1980),
    ("Cannibal Ferox", 1981),

    # Surrealismo / Vanguardia Europea
    ("Sedmikrásky", 1966),
    ("Valerie a týden divů", 1970),
    ("Santa Sangre", 1989),
    ("Possession", 1981),
    ("The Devils", 1971),
    ("Even Dwarfs Started Small", 1970),
    ("Un Chien Andalou", 1929),
    ("The Holy Mountain", 1973),
    ("Vampyros Lesbos", 1971),

    # Horror de Culto Latinoamericano
    ("À Meia-Noite Levarei Sua Alma", 1964),
    ("Esta Noite Encarnarei no Teu Cadáver", 1967),
    ("Alucarda", 1977),
    ("Veneno para las hadas", 1984),
    ("Más negro que la noche", 1975),

    # Cine de Culto Indie / Extraño
    ("Otto; or, Up with Dead People", 2008),
    ("Tales from the Gimli Hospital", 1988),
    ("Careful", 1992),
    ("The American Astronaut", 2001),
    ("Begotten", 1990),
    ("Pi", 1998),
    ("Primer", 2004),
    ("Coherence", 2013),
    ("Beyond the Black Rainbow", 2010),
    ("Mandy", 2018),

    # Clásicos de Medianoche y Horror Imprescindible
    ("The Evil Dead", 1981),
    ("Evil Dead II", 1987),
    ("The Wicker Man", 1973),
    ("The Texas Chain Saw Massacre", 1974),
    ("Night of the Living Dead", 1968),
    ("Dawn of the Dead", 1978),
    ("Day of the Dead", 1985),
    ("Re-Animator", 1985),
    ("From Beyond", 1986),
    ("Phantasm", 1979),
    ("Hellraiser", 1987),
    ("Jacob's Ladder", 1990),
    ("Donnie Darko", 2001),

    # --- 50 PELÍCULAS ADICIONALES ---

    # Fantasía Obscura / Cyberpunk / Sci-Fi de Culto
    ("Hardware", 1990),
    ("Liquid Sky", 1982),
    ("Dark City", 1998),
    ("eXistenZ", 1999),
    ("City of Lost Children", 1995),
    ("Fantastic Planet", 1973),
    ("Phase IV", 1974),
    ("World on a Wire", 1973),
    ("A Boy and His Dog", 1975),
    ("Silent Running", 1972),

    # Horror Corporal & Splatter Adicional
    ("The Fly", 1986),
    ("Street Trash", 1987),
    ("Dead Alive", 1992),
    ("Slither", 2006),
    ("Shivers", 1975),
    ("Rabid", 1977),
    ("Body Melt", 1993),
    ("Pieces", 1982),

    # Giallo / Euro-Horror Adicional
    ("The House with Laughing Windows", 1976),
    ("Don't Torture a Duckling", 1972),
    ("Phenomena", 1985),
    ("Opera", 1987),
    ("City of the Living Dead", 1980),
    ("The House by the Cemetery", 1981),
    ("Daughters of Darkness", 1971),
    ("Lizard in a Woman's Skin", 1971),

    # Cine Extremo / Arthouse Extremo Adicional
    ("Salo, or the 120 Days of Sodom", 1975),
    ("Climax", 2018),
    ("Raw", 2016),
    ("Titane", 2021),
    ("Funny Games", 1997),
    ("Visitor Q", 2001),
    ("Tetsuo: The Bullet Man", 2010),
    ("Rubber", 2010),

    # Folk Horror / Culto Oculto
    ("Witchfinder General", 1968),
    ("Blood on Satan's Claw", 1971),
    ("Midsommar", 2019),
    ("The Witch", 2015),
    ("Häxan", 1922),

    # Trash / Cine B / Grindhouse Adicional
    ("Plan 9 from Outer Space", 1957),
    ("Manos: The Hands of Fate", 1966),
    ("Killer Klowns from Outer Space", 1988),
    ("Hoboken Hollow", 2006),
    ("Poultrygeist: Night of the Chicken Dead", 2006),
    ("Cannibal! The Musical", 1993),
    ("Snoop Dogg's Hood of Horror", 2006),

    # Vanguardia / Surrealismo Adicional
    ("L'Age d'Or", 1930),
    ("La Jetée", 1962),
    ("Lucifer Rising", 1972),
    ("Inland Empire", 2006)
]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def buscar_pelicula(titulo: str, anio: int):
    resp = requests.get(
        f"{BASE_URL}/search/movie",
        params={"api_key": API_KEY, "query": titulo, "year": anio, "language": "es-ES"},
    )
    resp.raise_for_status()
    resultados = resp.json().get("results", [])
    return resultados[0] if resultados else None


def obtener_detalle(movie_id: int):
    resp = requests.get(
        f"{BASE_URL}/movie/{movie_id}",
        params={"api_key": API_KEY, "language": "es-ES"},
    )
    resp.raise_for_status()
    return resp.json()


def obtener_director(movie_id: int) -> str:
    resp = requests.get(
        f"{BASE_URL}/movie/{movie_id}/credits",
        params={"api_key": API_KEY},
    )
    resp.raise_for_status()
    crew = resp.json().get("crew", [])
    directores = [p["name"] for p in crew if p.get("job") == "Director"]
    return ", ".join(directores) if directores else ""


def construir_entrada(titulo: str, anio: int) -> dict | None:
    encontrada = buscar_pelicula(titulo, anio)
    if not encontrada:
        print(f"  ⚠ No se encontró: {titulo} ({anio})")
        return None

    detalle = obtener_detalle(encontrada["id"])
    director = obtener_director(encontrada["id"])
    paises = [p["name"] for p in detalle.get("production_countries", [])]

    return {
        "title": detalle.get("title", titulo),
        "year": anio,
        "slug": slugify(f"{titulo}-{anio}"),
        "director": director,
        "country": ", ".join(paises),
        "synopsis": detalle.get("overview", ""),
        "images": {
            "poster": f"{POSTER_BASE}{detalle['poster_path']}" if detalle.get("poster_path") else "",
        },
        "categories": [g["name"] for g in detalle.get("genres", [])],
        "runtime_minutes": detalle.get("runtime", 0),
        "metadata": {
            "cult_status": "",
            "format": "",
            "audio": detalle.get("original_language", ""),
        },
    }


def main():
    if not API_KEY:
        raise SystemExit("Falta la variable de entorno TMDB_API_KEY")

    peliculas = []
    total = len(CURATED_TITLES)
    print(f"Iniciando la descarga de {total} películas desde TMDB...\n")

    for idx, (titulo, anio) in enumerate(CURATED_TITLES, 1):
        print(f"[{idx}/{total}] Buscando: {titulo} ({anio})...")
        entrada = construir_entrada(titulo, anio)
        if entrada:
            peliculas.append(entrada)
        time.sleep(0.25)

    with open("peliculas.json", "w", encoding="utf-8") as f:
        json.dump(peliculas, f, ensure_ascii=False, indent=2)

    print(f"\n¡Proceso completado! Se guardaron {len(peliculas)} películas en peliculas.json")


if __name__ == "__main__":
    main()
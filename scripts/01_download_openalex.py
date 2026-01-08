#!/usr/bin/env python3
"""
01_download_openalex.py
Descarga literatura sobre transnacionalismo desde OpenAlex API
Proyecto Chernilo/Rivas - UAI/CEP

Uso:
    python 01_download_openalex.py

Output:
    data/transnationalism_openalex.csv
    data/transnationalism_abstracts.txt
"""

import requests
import json
import time
import csv
import os
from datetime import datetime

# Configuración
OUTPUT_DIR = "data"
SEARCH_TERM = "transnationalism"
YEAR_START = 1990
YEAR_END = 2024
MAX_PAGES = 150  # ~30,000 registros

def fetch_page(cursor="*", per_page=200):
    """Fetch una página de OpenAlex con reintentos"""
    base_url = "https://api.openalex.org/works"
    filters = f"abstract.search:{SEARCH_TERM},publication_year:{YEAR_START}-{YEAR_END},type:article"
    params = {
        "filter": filters,
        "per_page": per_page,
        "cursor": cursor,
        "select": "id,doi,title,publication_year,authorships,primary_location,abstract_inverted_index,cited_by_count",
        "mailto": "tu-email@ejemplo.com"  # Recomendado por OpenAlex para mejor rate limit
    }
    
    for attempt in range(3):
        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f" (intento {attempt+1} falló: {e})", end="")
            time.sleep(2 ** attempt)
    return None

def reconstruct_abstract(inverted_index):
    """Reconstruir abstract desde formato de índice invertido de OpenAlex"""
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join([word for _, word in word_positions])

def get_authors(authorships, max_authors=5):
    """Extraer nombres de autores"""
    if not authorships:
        return ""
    authors = []
    for auth in authorships[:max_authors]:
        name = auth.get("author", {}).get("display_name")
        if name:
            authors.append(name)
    return "; ".join(authors)

def get_journal(primary_location):
    """Extraer nombre de revista"""
    if not primary_location:
        return ""
    source = primary_location.get("source", {})
    return source.get("display_name", "") if source else ""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"{'='*60}")
    print(f"DESCARGA DE LITERATURA: {SEARCH_TERM.upper()}")
    print(f"Período: {YEAR_START}-{YEAR_END}")
    print(f"{'='*60}")
    print(f"Inicio: {datetime.now()}\n")
    
    csv_path = os.path.join(OUTPUT_DIR, "transnationalism_openalex.csv")
    abstracts_path = os.path.join(OUTPUT_DIR, "transnationalism_abstracts.txt")
    
    cursor = "*"
    page = 0
    total_works = 0
    total_abstracts = 0
    first_batch = True
    
    csv_file = open(csv_path, "w", newline="", encoding="utf-8")
    abstracts_file = open(abstracts_path, "w", encoding="utf-8")
    
    fieldnames = ["id", "doi", "title", "year", "authors", "journal", "cited_by_count", "abstract"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    while True:
        page += 1
        print(f"Página {page}...", end=" ", flush=True)
        
        data = fetch_page(cursor)
        
        if not data:
            print("ERROR")
            break
        
        results = data.get("results", [])
        if not results:
            print("Sin más resultados.")
            break
        
        # Procesar batch
        for work in results:
            abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
            
            record = {
                "id": work.get("id", "").replace("https://openalex.org/", ""),
                "doi": work.get("doi", ""),
                "title": work.get("title", ""),
                "year": work.get("publication_year", ""),
                "authors": get_authors(work.get("authorships")),
                "journal": get_journal(work.get("primary_location")),
                "cited_by_count": work.get("cited_by_count", 0),
                "abstract": abstract
            }
            writer.writerow(record)
            total_works += 1
            
            if abstract:
                abstracts_file.write(abstract + "\n")
                total_abstracts += 1
        
        print(f"{len(results)} reg. | Total: {total_works}")
        
        # Siguiente cursor
        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            print("Fin de paginación.")
            break
        
        time.sleep(0.1)  # Rate limiting
        
        if page >= MAX_PAGES:
            print(f"Límite de {MAX_PAGES} páginas alcanzado.")
            break
    
    csv_file.close()
    abstracts_file.close()
    
    print(f"\n{'='*60}")
    print(f"DESCARGA COMPLETADA")
    print(f"{'='*60}")
    print(f"Total trabajos: {total_works}")
    print(f"Total abstracts: {total_abstracts}")
    print(f"Archivos: {csv_path}, {abstracts_path}")
    print(f"Fin: {datetime.now()}")

if __name__ == "__main__":
    main()

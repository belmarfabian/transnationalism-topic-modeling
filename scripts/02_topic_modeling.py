#!/usr/bin/env python3
"""
02_topic_modeling.py
Topic Modeling con LDA para literatura de transnacionalismo
Proyecto Chernilo/Rivas - UAI/CEP

Uso:
    python 02_topic_modeling.py

Input:
    data/transnationalism_openalex.csv

Output:
    data/transnationalism_topics.csv
    outputs/topic_summary.json
"""

import pandas as pd
import numpy as np
import re
import json
import os
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import warnings
warnings.filterwarnings('ignore')

# Configuración
N_TOPICS = 15
DATA_DIR = "data"
OUTPUT_DIR = "outputs"

# Stopwords expandidas para literatura académica
STOPWORDS = [
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'this', 'that', 'these', 'those', 'it', 'its', 'they', 'their', 'them', 'we', 'our',
    'i', 'you', 'he', 'she', 'his', 'her', 'which', 'who', 'whom', 'what', 'where', 'when',
    'how', 'why', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    'can', 'just', 'also', 'into', 'over', 'after', 'before', 'between', 'through',
    'during', 'above', 'below', 'up', 'down', 'out', 'off', 'about', 'against', 'further',
    # Academic stopwords
    'article', 'paper', 'study', 'research', 'analysis', 'examine', 'examines', 'examined',
    'explore', 'explores', 'explored', 'investigate', 'investigates', 'investigated',
    'argue', 'argues', 'argued', 'suggest', 'suggests', 'suggested', 'show', 'shows', 'shown',
    'find', 'finds', 'found', 'discuss', 'discusses', 'discussed', 'focus', 'focuses', 'focused',
    'based', 'using', 'used', 'use', 'approach', 'method', 'data', 'case', 'cases',
    'however', 'although', 'thus', 'therefore', 'moreover', 'furthermore', 'nevertheless',
    'particularly', 'especially', 'specifically', 'generally', 'often', 'always', 'never',
    'many', 'much', 'several', 'various', 'different', 'similar', 'new', 'first', 'second',
    'well', 'within', 'without', 'among', 'across', 'while', 'since', 'because', 'whether',
    'one', 'two', 'three', 'way', 'ways', 'form', 'forms', 'part', 'parts', 'role', 'roles',
    'understanding', 'relationship', 'relationships', 'perspective', 'perspectives',
    'context', 'contexts', 'process', 'processes', 'important', 'significant', 'key',
    'particular', 'certain', 'given', 'present', 'current', 'recent', 'provides', 'provide'
]

def preprocess(text):
    """Limpiar texto para topic modeling"""
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-záéíóúñü\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_top_words(model, feature_names, n_top=15):
    """Extraer palabras principales de cada tópico"""
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        top_indices = topic.argsort()[:-n_top-1:-1]
        top_words = [feature_names[i] for i in top_indices]
        topics.append(top_words)
    return topics

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 60)
    print(f"TOPIC MODELING: TRANSNACIONALISMO")
    print("=" * 60)
    
    # Cargar datos
    input_path = os.path.join(DATA_DIR, "transnationalism_openalex.csv")
    df = pd.read_csv(input_path)
    print(f"\nDatos cargados: {len(df)} registros")
    
    # Filtrar
    df = df[df['abstract'].notna() & (df['abstract'].str.len() > 100)].copy()
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df[df['year'].notna()].copy()
    df['year'] = df['year'].astype(int)
    print(f"Con abstracts válidos: {len(df)} registros")
    
    # Preprocesar
    df['clean_text'] = df['abstract'].apply(preprocess)
    
    # Vectorización
    print("\nVectorizando...")
    vectorizer = CountVectorizer(
        max_df=0.85,
        min_df=20,
        max_features=5000,
        stop_words=STOPWORDS,
        ngram_range=(1, 2)
    )
    
    doc_term_matrix = vectorizer.fit_transform(df['clean_text'])
    feature_names = vectorizer.get_feature_names_out()
    print(f"Vocabulario: {len(feature_names)} términos")
    
    # LDA
    print(f"\nEntrenando LDA con {N_TOPICS} tópicos...")
    lda = LatentDirichletAllocation(
        n_components=N_TOPICS,
        max_iter=25,
        learning_method='online',
        random_state=42,
        n_jobs=-1
    )
    
    doc_topics = lda.fit_transform(doc_term_matrix)
    
    # Asignar tópicos
    df['dominant_topic'] = doc_topics.argmax(axis=1)
    df['topic_prob'] = doc_topics.max(axis=1)
    
    # Extraer palabras por tópico
    topic_words = get_top_words(lda, feature_names, 15)
    
    print("\n" + "=" * 60)
    print("TÓPICOS IDENTIFICADOS")
    print("=" * 60)
    
    topic_summary = []
    for i, words in enumerate(topic_words):
        count = (df['dominant_topic'] == i).sum()
        pct = 100 * count / len(df)
        print(f"\nT{i:02d} ({pct:5.1f}%): {', '.join(words[:10])}")
        topic_summary.append({
            'topic_id': i,
            'count': int(count),
            'percentage': round(pct, 2),
            'top_words': words
        })
    
    # Guardar resultados
    output_csv = os.path.join(DATA_DIR, "transnationalism_topics.csv")
    df_export = df[['id', 'doi', 'title', 'year', 'authors', 'journal', 
                    'cited_by_count', 'dominant_topic', 'topic_prob']].copy()
    df_export.to_csv(output_csv, index=False)
    print(f"\n✓ {output_csv}")
    
    output_json = os.path.join(OUTPUT_DIR, "topic_summary.json")
    with open(output_json, "w") as f:
        json.dump(topic_summary, f, indent=2)
    print(f"✓ {output_json}")
    
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()

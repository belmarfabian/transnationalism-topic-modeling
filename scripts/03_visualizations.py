#!/usr/bin/env python3
"""
03_visualizations.py
Genera visualizaciones interactivas para el análisis de transnacionalismo
Proyecto Chernilo/Rivas - UAI/CEP

Uso:
    python 03_visualizations.py

Input:
    data/transnationalism_topics.csv

Output:
    figures/fig_temporal.html
    figures/fig_divergent.html
    figures/fig_stacked.html
    figures/fig_volume.html
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Configuración
DATA_DIR = "data"
FIGURES_DIR = "figures"

# Etiquetas interpretativas
TOPIC_LABELS = {
    0: 'Migración y Familia',
    1: 'Educación y Derechos',
    2: 'Derecho y Gobernanza',
    3: 'Movimientos Sociales',
    4: 'Teoría y Estudios',
    5: 'Corporaciones',
    6: 'Salud/Política',
    7: 'Terrorismo/Rel.Int.',
    8: 'Media Digital',
    9: 'Cultural/Sur Global',
    10: 'Inmigración',
    11: 'EEUU/México',
    12: 'Economía/China',
    13: 'Diáspora/Historia',
    14: 'Género/Feminismo'
}

COLORS = {
    0: '#e41a1c',   # Rojo - Migración
    1: '#f781bf',   # Rosa - Educación
    2: '#377eb8',   # Azul - Derecho
    3: '#ff7f00',   # Naranja - Movimientos
    4: '#4daf4a',   # Verde - Teoría
    7: '#984ea3',   # Púrpura - Terrorismo
    8: '#00CED1',   # Turquesa - Media
    9: '#FFD700',   # Dorado - Cultural
    12: '#2F4F4F',  # Gris oscuro - Economía
    13: '#999999'   # Gris - Diáspora
}

def smooth(series, window=3):
    """Media móvil para suavizar series temporales"""
    return series.rolling(window=window, center=True, min_periods=1).mean()

def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    
    print("=" * 60)
    print("GENERANDO VISUALIZACIONES")
    print("=" * 60)
    
    # Cargar datos
    df = pd.read_csv(os.path.join(DATA_DIR, "transnationalism_topics.csv"))
    print(f"Registros: {len(df)}")
    
    # Calcular proporciones anuales
    yearly = df.groupby(['year', 'dominant_topic']).size().unstack(fill_value=0)
    yearly_pct = yearly.div(yearly.sum(axis=1), axis=0) * 100
    
    # ================================================================
    # Figura 1: Evolución temporal principal
    # ================================================================
    print("\nGenerando fig_temporal.html...")
    
    fig1 = go.Figure()
    for t in [4, 2, 9, 0, 7, 13]:
        col = str(t)
        if col in yearly_pct.columns:
            y_smooth = smooth(yearly_pct[col])
            fig1.add_trace(go.Scatter(
                x=yearly_pct.index.tolist(),
                y=y_smooth.tolist(),
                mode='lines',
                name=TOPIC_LABELS[t],
                line=dict(color=COLORS.get(t, '#333'), width=2.5)
            ))
    
    fig1.update_layout(
        title='<b>Evolución de Tópicos en Transnacionalismo (1990-2024)</b><br><sup>Proporción anual (%), suavizado 3 años, N=21,394</sup>',
        xaxis=dict(title='Año', range=[1990, 2024], dtick=5),
        yaxis=dict(title='Proporción (%)', range=[0, 35]),
        legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center'),
        template='plotly_white',
        width=1000,
        height=550,
        hovermode='x unified'
    )
    
    fig1.write_html(os.path.join(FIGURES_DIR, "fig_temporal.html"), include_plotlyjs=True)
    print("✓ fig_temporal.html")
    
    # ================================================================
    # Figura 2: Tendencias divergentes
    # ================================================================
    print("Generando fig_divergent.html...")
    
    fig2 = make_subplots(
        rows=2, cols=1,
        subplot_titles=('<b>Tópicos Emergentes</b>', '<b>Tópicos en Declive</b>'),
        vertical_spacing=0.12
    )
    
    for t in [0, 4, 1]:
        col = str(t)
        if col in yearly_pct.columns:
            fig2.add_trace(go.Scatter(
                x=yearly_pct.index.tolist(),
                y=smooth(yearly_pct[col]).tolist(),
                name=TOPIC_LABELS[t],
                line=dict(color=COLORS.get(t, '#333'), width=2)
            ), row=1, col=1)
    
    for t in [12, 7, 2]:
        col = str(t)
        if col in yearly_pct.columns:
            fig2.add_trace(go.Scatter(
                x=yearly_pct.index.tolist(),
                y=smooth(yearly_pct[col]).tolist(),
                name=TOPIC_LABELS[t],
                line=dict(color=COLORS.get(t, '#333'), width=2)
            ), row=2, col=1)
    
    fig2.update_layout(
        height=650,
        template='plotly_white',
        legend=dict(orientation='h', y=-0.12, x=0.5, xanchor='center'),
        hovermode='x unified'
    )
    fig2.update_xaxes(range=[1990, 2024])
    
    fig2.write_html(os.path.join(FIGURES_DIR, "fig_divergent.html"), include_plotlyjs=True)
    print("✓ fig_divergent.html")
    
    # ================================================================
    # Figura 3: Área apilada
    # ================================================================
    print("Generando fig_stacked.html...")
    
    fig3 = go.Figure()
    for t in [4, 2, 9, 0, 7, 13, 1, 12]:
        col = str(t)
        if col in yearly_pct.columns:
            fig3.add_trace(go.Scatter(
                x=yearly_pct.index.tolist(),
                y=yearly_pct[col].tolist(),
                name=TOPIC_LABELS[t],
                stackgroup='one',
                line=dict(width=0.5)
            ))
    
    fig3.update_layout(
        title='<b>Composición Temática del Campo (1990-2024)</b>',
        xaxis=dict(title='Año', range=[1990, 2024]),
        yaxis=dict(title='Proporción (%)', range=[0, 100]),
        template='plotly_white',
        height=550,
        hovermode='x unified',
        legend=dict(x=1.02, y=1)
    )
    
    fig3.write_html(os.path.join(FIGURES_DIR, "fig_stacked.html"), include_plotlyjs=True)
    print("✓ fig_stacked.html")
    
    # ================================================================
    # Figura 4: Volumen + tendencias
    # ================================================================
    print("Generando fig_volume.html...")
    
    fig4 = make_subplots(
        rows=2, cols=1,
        row_heights=[0.3, 0.7],
        subplot_titles=('<b>Volumen Anual de Publicaciones</b>', '<b>Tópicos Principales</b>'),
        vertical_spacing=0.1
    )
    
    yearly_counts = df.groupby('year').size()
    fig4.add_trace(go.Bar(
        x=yearly_counts.index.tolist(),
        y=yearly_counts.values.tolist(),
        marker_color='#3498db',
        showlegend=False
    ), row=1, col=1)
    
    for t in [4, 0, 2, 9]:
        col = str(t)
        if col in yearly_pct.columns:
            fig4.add_trace(go.Scatter(
                x=yearly_pct.index.tolist(),
                y=smooth(yearly_pct[col]).tolist(),
                name=TOPIC_LABELS[t],
                line=dict(color=COLORS.get(t, '#333'), width=2)
            ), row=2, col=1)
    
    fig4.update_layout(
        height=700,
        template='plotly_white',
        legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center'),
        hovermode='x unified'
    )
    fig4.update_xaxes(range=[1990, 2024])
    
    fig4.write_html(os.path.join(FIGURES_DIR, "fig_volume.html"), include_plotlyjs=True)
    print("✓ fig_volume.html")
    
    print("\n" + "=" * 60)
    print("VISUALIZACIONES COMPLETADAS")
    print("=" * 60)

if __name__ == "__main__":
    main()

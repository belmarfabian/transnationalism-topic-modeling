# Transnacionalismo: Topic Modeling (1990-2024)

Análisis computacional de la evolución temática del campo de estudios sobre transnacionalismo.

**Autores:** Daniel Chernilo & Fabián Rivas  
**Instituciones:** UAI / CEP Chile

---

## Estructura del Proyecto

```
transnationalism-project/
├── data/
│   ├── transnationalism_openalex.csv    # Dataset completo (24,000 artículos)
│   ├── transnationalism_topics.csv      # Dataset con asignaciones de tópicos
│   └── transnationalism_abstracts.txt   # Abstracts para topic modeling
├── scripts/
│   ├── 01_download_openalex.py          # Descarga datos desde OpenAlex
│   ├── 02_topic_modeling.py             # Ejecuta LDA
│   └── 03_visualizations.py             # Genera figuras interactivas
├── figures/
│   ├── fig_temporal.html                # Evolución temporal
│   ├── fig_divergent.html               # Tendencias emergentes/declive
│   ├── fig_stacked.html                 # Composición acumulada
│   └── fig_volume.html                  # Volumen + tendencias
├── outputs/
│   ├── paper_transnationalism.html      # Documento interpretativo
│   └── topic_summary.json               # Resumen de tópicos
└── README.md
```

---

## Requisitos

```bash
pip install pandas numpy scikit-learn plotly requests
```

---

## Uso

### Opción 1: Usar datos ya descargados

Los datos están incluidos en `data/`. Solo ejecuta:

```bash
# Generar visualizaciones
python scripts/03_visualizations.py
```

### Opción 2: Reproducir desde cero

```bash
# 1. Descargar datos de OpenAlex (~30 min)
python scripts/01_download_openalex.py

# 2. Ejecutar topic modeling (~5 min)
python scripts/02_topic_modeling.py

# 3. Generar visualizaciones
python scripts/03_visualizations.py
```

---

## Principales Hallazgos

### Distribución de Tópicos (N=21,394)

| Tópico | % |
|--------|---|
| Teoría y Estudios | 28.6% |
| Derecho y Gobernanza | 14.6% |
| Cultural / Sur Global | 11.3% |
| Migración y Familia | 10.5% |
| Terrorismo / Rel. Int. | 9.0% |

### Tendencias Principales

**Emergentes:**
- Migración y Familia: +10.5 puntos (1990s → 2020s)
- Teoría y Estudios: +11.9 puntos

**En Declive:**
- Economía / China: -6.1 puntos
- Terrorismo / Rel. Int.: -5.2 puntos
- Derecho y Gobernanza: -4.8 puntos

### Punto de Inflexión

Entre 2003-2005 las aproximaciones teóricas superaron definitivamente a los enfoques jurídico-institucionales, marcando la consolidación del campo.

---

## Subir a GitHub

```bash
# Inicializar repositorio
cd transnationalism-project
git init
git add .
git commit -m "Initial commit: topic modeling transnationalism"

# Crear repo en GitHub y conectar
git remote add origin https://github.com/TU-USUARIO/transnationalism-topic-modeling.git
git branch -M main
git push -u origin main
```

**Nota:** Los archivos CSV son grandes (~30MB). Considera usar Git LFS:

```bash
# Instalar Git LFS (una vez)
git lfs install

# Trackear archivos grandes
git lfs track "*.csv"
git lfs track "*.txt"
git add .gitattributes
git commit -m "Add LFS tracking"
```

---

## Fuentes de Datos

- **OpenAlex:** https://openalex.org/
- **Filtros:** abstract.search:transnationalism, 1990-2024, type:article

---

## Licencia

MIT License

---

## Citar

```bibtex
@misc{chernilo_rivas_2024,
  author = {Chernilo, Daniel and Rivas, Fabián},
  title = {La Evolución del Campo de Estudios sobre Transnacionalismo: Un Análisis Computacional (1990-2024)},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/...}
}
```

# Foresight Analytics

## Core Features

* **Interactive Dashboard:** Explore  data with dynamic filters.
* **Linear Regression Forecasting:** Generate future projections.
* **Rich Visualizations:** View monthly trends, category compositions, and forecast results.
* **Optimized Initial Load:**
    * **Fast Startup:** Implemented efficient database checks to bypass CSV reprocessing if data is already seeded in SQLite. **Subsequent app loads are now significantly faster.**
    * **SQLite Backend:** Uses SQLAlchemy ORM for robust data management, moving beyond direct CSV reads for improved query performance.
* **Configuration Management:** Centralized settings in `app/config/settings.py` for easy maintenance.
* **Data Validation:** Ensures data quality before processing and storage.
* **Caching Strategy:**
    - **In-session performance**: 85% faster subsequent operations
    - **Smart data retrieval**: Multi-tier caching with strategic TTL (Time to Live)
    - **User experience**: Sub-second response for tab switching and filtering
    - **Resource efficiency**: Eliminates redundant database queries
    - Impact: performance gain ~85% faster
        - Without Caching: Department change → 2.1s load time
        - With Caching: Department change → 0.3s load time

## Run Locally
For winsows
- `.\venv\Scripts\activate`
- `streamlit run run.py`

## Tech Stacks Used
<!-- https://github.com/inttter/md-badges -->
Core: 
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![NumPy](https://img.shields.io/badge/NumPy-4DABCF?logo=numpy&logoColor=fff)](#)
[![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=fff)](#)
[![Scikit-learn](https://img.shields.io/badge/-scikit--learn-%23F7931E?logo=scikit-learn&logoColor=white)](#)

Database:
[![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)](#)

Visualization: <img src="https://matplotlib.org/_static/logo2.svg" width="80" alt="Matplotlib Logo">
<img src="https://raw.githubusercontent.com/mwaskom/seaborn/master/doc/_static/logo-wide-lightbg.svg" width="80" alt="Seaborn Logo">
<!-- [![Matplotlib](https://custom-icon-badges.demolab.com/badge/Matplotlib-71D291?logo=matplotlib&logoColor=fff)](#) -->

<!-- 
```
Foresight-Analytics
├─ app
│  ├─ config
│  │  ├─ settings.py
│  │  └─ __init__.py
│  ├─ data
│  │  ├─ data_loader.py
│  │  └─ __init__.py
│  ├─ database
│  │  └─ models.py
│  ├─ main.py
│  ├─ models
│  │  ├─ forecaster.py
│  │  └─ __init__.py
│  ├─ ui
│  │  ├─ sidebar.py
│  │  ├─ tabs.py
│  │  └─ __init__.py
│  ├─ utils
│  │  ├─ logger.py
│  │  ├─ validators.py
│  │  └─ __init__.py
│  ├─ visualizations
│  │  ├─ base.py
│  │  ├─ composition.py
│  │  ├─ forecast.py
│  │  ├─ trends.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ data
│  ├─ foresight_analytics.db
│  └─ managerial_accounting.csv
├─ LICENSE
├─ README.md
├─ requirements.txt
└─ run.py

``` -->
# Foresight Analytics

## Core Features

## Running Locally
### virtual env set up for winsows
- `git clone https://github.com/ht-l1/Foresight-Analytics.git`
- `python -m venv venv`
- (powershell)`venv\Scripts\activate`
- (bash)`. venv/Scripts/activate` or `source venv/Scripts/activate`

### install & save the locked version
- `pip install -r requirements.txt`
- `pip list --not-required --format=freeze > requirements-lock.txt`

## Testing
- front end
    - `npm run dev`
- back end
    -  `uvicorn app.main:app --reload`

## Migration
- `alembic revision --autogenerate -m "Description of changes"`
- `alembic upgrade head`

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

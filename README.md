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

## Docker 
- `docker-compose up`

## Migration at powershell
- `docker-compose exec backend /bin/bash`
- `alembic revision --autogenerate -m "Description of changes"`
- `alembic upgrade head`

## Tech Stacks Used
<!-- https://github.com/inttter/md-badges -->
Core: 
Database:
Visualization:
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip

# Copy app code
COPY . .

# Use non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Copy .env.example for reference (not for production use)
# COPY .env.example /app/.env.example

# Healthcheck (optional, for Docker Compose/K8s)
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# For development, use uvicorn; for production, recommend gunicorn (commented)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
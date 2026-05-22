# Standalone agent image (shared-core bundled at agent creation).
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/shared-core

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared-core ./shared-core
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build from lab root:
#   docker build -f agent-template/Dockerfile -t agent-template .
#
# Build a generated agent from its folder (shared-core bundled by create-agent):
#   cd agents/quality-inspector && docker build -t quality-inspector .
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/shared-core

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Lab-root build (paths relative to repo root)
COPY shared-core ./shared-core
COPY agent-template/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

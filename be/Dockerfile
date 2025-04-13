# Base stage with system dependencies
FROM python:3.9-slim as base
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dependencies stage that will be cached
FROM base as deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Tag this stage for reuse
FROM deps as runtime-deps

# Final stage
FROM python:3.9-slim as final
WORKDIR /app

# Copy only runtime system dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from the tagged deps image
COPY --from=runtime-deps /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=runtime-deps /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

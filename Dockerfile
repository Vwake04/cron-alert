# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create logs directory
RUN mkdir -p logs

# Copy the rest of the application
COPY . .

# Create a volume for SQLite database if used
VOLUME /app/data
VOLUME /app/logs

# Set default environment variables
ENV PYTHONUNBUFFERED=1
ENV DB_TYPE=sqlite
ENV DB_PATH=/app/data/db.sqlite3
ENV SQL_ECHO=false

# Example PostgreSQL environment variables (commented out by default)
# ENV DB_TYPE=postgresql
# ENV DB_USER=postgres
# ENV DB_PASSWORD=password
# ENV DB_HOST=localhost
# ENV DB_PORT=5432
# ENV DB_NAME=upgrades

CMD ["python", "app.py"] 
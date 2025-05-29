FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    postgresql \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Final stage
FROM python:3.11-slim

WORKDIR /usr/src/app

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    netcat-traditional \
    postgresql \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Add entrypoint script
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
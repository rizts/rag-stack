FROM python:3.11-slim

WORKDIR /app

# Env variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .
RUN chmod +x start.sh
CMD ["./start.sh"]

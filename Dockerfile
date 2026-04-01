# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but good practice)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports (if needed)
# IoT Edge / Modbus / OCPP (optional)
EXPOSE 8883
EXPOSE 502
EXPOSE 3000

# Run the application
CMD ["python", "src/main.py"]
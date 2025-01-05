# Use official Python image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    mariadb-client \
    curl \
    net-tools \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set backend port environment variable
ENV BACKEND_INTERNAL_PORT=5001

# Expose the Flask app port
EXPOSE ${BACKEND_INTERNAL_PORT}

# Run the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:${BACKEND_INTERNAL_PORT}", "server:app"]

# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies, including MariaDB client, curl, net-tools, and iproute2
RUN apt-get update && apt-get install -y \
    mariadb-client \
    curl \
    net-tools \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default environment variable for BACKEND_INTERNAL_PORT
# ENV BACKEND_INTERNAL_PORT=5000
ENV BACKEND_INTERNAL_PORT=5001

# Expose the port for the Flask app
EXPOSE ${BACKEND_INTERNAL_PORT}

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:${BACKEND_INTERNAL_PORT}", "server:app"]

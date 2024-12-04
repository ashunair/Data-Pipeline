# Use an official Python image as the base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY pubsub_publisher.py /app

# Install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for GCP credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/data-pipleine-keys.json

# Copy the GCP service account key file (add this securely, not in production)
COPY data-pipleine-keys.json /app

# Set the default command to run the publisher script
CMD ["python", "pubsub_publisher.py"]

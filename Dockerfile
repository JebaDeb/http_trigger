# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port for Flask
EXPOSE 8080

# Set environment variable for Flask
ENV PORT 8080

# Start the Flask app
CMD ["python", "main.py"]


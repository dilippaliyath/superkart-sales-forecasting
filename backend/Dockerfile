FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to improve Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application and model files
COPY . .

# Document the port used by the application
EXPOSE 7860

# Start Flask application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]

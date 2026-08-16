
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies first for better Docker caching
COPY requirements.txt .

# Install frontend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Start the Streamlit application
CMD [
    "streamlit",
    "run",
    "app.py",
    "--server.address=0.0.0.0",
    "--server.port=8501"
]

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY export_tasks.py .

# Create tasks directory
RUN mkdir -p /app/tasks

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the export script
ENTRYPOINT ["python", "export_tasks.py"]

FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
COPY chroma_db .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY query.py .

# Make port 8080 available
EXPOSE 8080

# Run the application
CMD ["python", "query.py"]
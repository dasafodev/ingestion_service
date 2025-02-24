FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a volume for the SQLite database
VOLUME /app/data

# Set environment variable for database
ENV DATABASE_URL=sqlite:///data/ingestion_service.db

EXPOSE 5001

CMD ["python", "main.py"]
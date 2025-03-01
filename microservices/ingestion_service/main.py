#!/usr/bin/env python
# microservices/ingestion_service/main.py
from flask import Flask, request, jsonify
import os
import sys

# Add the root directory to the path so we can import from the main project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from application.services import DataIngestionService
from infrastructure.repositories_impl import SQLAlchemyDataRepository
from infrastructure.event_bus import PulsarEventBus
from infrastructure.database import create_tables
from domain.events import DataIngested

app = Flask(__name__)

# Initialize database
create_tables()

# Initialize repositories and services
data_repo = SQLAlchemyDataRepository()

# Initialize Pulsar event bus
pulsar_service_url = os.environ.get('PULSAR_SERVICE_URL', 'pulsar://localhost:6650')
event_bus = PulsarEventBus(service_url=pulsar_service_url, client_id="ingestion-service")

def log_data_ingested(event):
    print(f"Event received: DataIngested - ID: {event.data_id}, Partner: {event.partner_id}")

# Subscribe to events (for local testing/debugging)
event_bus.subscribe(DataIngested, log_data_ingested)

# Initialize services
data_service = DataIngestionService(data_repo, event_bus)

@app.route("/ingest", methods=["POST"])
def ingest():
    """Endpoint to ingest new data"""
    data_json = request.get_json()
    partner_id = data_json.get("partner_id")
    payload = data_json.get("payload")
    if not partner_id or payload is None:
        return jsonify({"error": "Se requieren 'partner_id' y 'payload'"}), 400

    data = data_service.ingest_data(partner_id, payload)
    return jsonify({
        "id": data.id,
        "partner_id": data.partner_id.value,
        "timestamp": data.timestamp.value.isoformat()
    }), 201

@app.route("/")
def index():
    """Root endpoint"""
    return "Data Ingestion Microservice - Hexagonal Architecture with Apache Pulsar"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 
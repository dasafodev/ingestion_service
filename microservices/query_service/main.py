#!/usr/bin/env python
# microservices/query_service/main.py
from flask import Flask, jsonify
import os
import sys

# Add the root directory to the path so we can import from the main project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from application.services import QueryService
from infrastructure.repositories_impl import SQLAlchemyDataRepository
from infrastructure.event_bus import PulsarEventBus
from domain.events import DataIngested

app = Flask(__name__)

# Initialize repositories and services
data_repo = SQLAlchemyDataRepository()

# Initialize Pulsar event bus
pulsar_service_url = os.environ.get('PULSAR_SERVICE_URL', 'pulsar://localhost:6650')
event_bus = PulsarEventBus(service_url=pulsar_service_url, client_id="query-service")

# Initialize services
query_service = QueryService(data_repo)

# Subscribe to events from the ingestion service
def handle_data_ingested(event):
    print(f"Query service received DataIngested event - ID: {event.data_id}, Partner: {event.partner_id}")
    # You could update a cache or perform other actions when new data is ingested

event_bus.subscribe(DataIngested, handle_data_ingested)

@app.route("/query/<data_id>", methods=["GET"])
def get_ingested_data(data_id):
    """Endpoint to get ingested data by ID"""
    data = query_service.get_data_by_id(data_id)
    if not data:
        return jsonify({"error": "Datos no encontrados"}), 404
    return jsonify({
        "id": data.id,
        "partner_id": data.partner_id.value,
        "timestamp": data.timestamp.value.isoformat(),
        "payload": data.payload.value
    })

@app.route("/query/partner/<partner_id>", methods=["GET"])
def get_data_by_partner(partner_id):
    """Endpoint to get all data for a specific partner"""
    data_list = query_service.get_data_by_partner_id(partner_id)
    return jsonify([{
        "id": data.id,
        "partner_id": data.partner_id.value,
        "timestamp": data.timestamp.value.isoformat()
    } for data in data_list])

@app.route("/query/all", methods=["GET"])
def get_all_data():
    """Endpoint to get all ingested data"""
    data_list = query_service.get_all_data()
    return jsonify([{
        "id": data.id,
        "partner_id": data.partner_id.value,
        "timestamp": data.timestamp.value.isoformat()
    } for data in data_list])

@app.route("/")
def index():
    """Root endpoint"""
    return "Data Query Microservice - Hexagonal Architecture with Apache Pulsar"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True) 
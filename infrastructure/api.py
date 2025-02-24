# infrastructure/api.py
from flask import Flask, request, jsonify
from application.services import DataIngestionService, QueryService
from infrastructure.repositories_impl import SQLAlchemyDataRepository
from infrastructure.event_bus import SimpleEventBus
from infrastructure.database import create_tables
from domain.events import DataIngested

app = Flask(__name__)

# Initialize database
create_tables()

# Initialize repositories and services
data_repo = SQLAlchemyDataRepository()
event_bus = SimpleEventBus()

def log_data_ingested(event):
    print(f"Event received: DataIngested - ID: {event.data_id}, Partner: {event.partner_id}")

event_bus.subscribe(DataIngested, log_data_ingested)

# Initialize services
data_service = DataIngestionService(data_repo, event_bus)
query_service = QueryService(data_repo)

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

@app.route("/ingest/<data_id>", methods=["GET"])
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

@app.route("/ingest/partner/<partner_id>", methods=["GET"])
def get_data_by_partner(partner_id):
    """Endpoint to get all data for a specific partner"""
    data_list = query_service.get_data_by_partner_id(partner_id)
    return jsonify([{
        "id": data.id,
        "partner_id": data.partner_id.value,
        "timestamp": data.timestamp.value.isoformat()
    } for data in data_list])

@app.route("/ingest/all", methods=["GET"])
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
    return "Data Ingestion Service - Hexagonal Architecture"

if __name__ == '__main__':
    app.run(debug=True)
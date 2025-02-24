# infrastructure/api.py
from flask import Flask, request, jsonify
from application.services import DataIngestionService
from infrastructure.repositories_impl import InMemoryDataRepository
from infrastructure.event_bus import SimpleEventBus
from domain.events import DataIngested

app = Flask(__name__)

data_repo = InMemoryDataRepository()
event_bus = SimpleEventBus()

def log_data_ingested(event):
    print(f"Evento recibido: DataIngested - ID: {event.data_id}, Partner: {event.partner_id}")

event_bus.subscribe(DataIngested, log_data_ingested)


data_service = DataIngestionService(data_repo, event_bus)

@app.route("/ingest", methods=["POST"])
def ingest():
    data_json = request.get_json()
    partner_id = data_json.get("partner_id")
    payload = data_json.get("payload")
    if not partner_id or payload is None:
        return jsonify({"error": "Se requieren 'partner_id' y 'payload'"}), 400

    data = data_service.ingest_data(partner_id, payload)
    return jsonify({
        "id": data.id,
        "partner_id": data.partner_id,
        "timestamp": data.timestamp.isoformat()
    }), 201

@app.route("/ingest/<data_id>", methods=["GET"])
def get_ingested_data(data_id):
    data = data_repo.get_by_id(data_id)
    if not data:
        return jsonify({"error": "Datos no encontrados"}), 404
    return jsonify({
        "id": data.id,
        "partner_id": data.partner_id,
        "timestamp": data.timestamp.isoformat(),
        "payload": data.payload
    })

@app.route("/")
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
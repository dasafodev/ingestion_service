#!/usr/bin/env python
# microservices/processing_service/main.py
import os
import sys
import time
import signal
import threading

# Add the root directory to the path so we can import from the main project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from infrastructure.event_bus import PulsarEventBus
from domain.events import DataIngested, DataProcessed
from infrastructure.repositories_impl import SQLAlchemyDataRepository

# Flag to control the main loop
running = True

def signal_handler(sig, frame):
    """Handle termination signals"""
    global running
    print("Shutting down processing service...")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def process_data(data_id, partner_id, timestamp):
    """
    Simulate data processing
    In a real application, this would perform actual processing on the data
    """
    print(f"Processing data: {data_id} from partner {partner_id}")
    
    # Simulate processing time
    time.sleep(2)
    
    # Return a simulated result
    return {
        "processed": True,
        "data_id": data_id,
        "partner_id": partner_id,
        "processing_timestamp": time.time(),
        "result": f"Processed data {data_id} successfully"
    }

def main():
    """Main function for the processing service"""
    print("Starting data processing service...")
    
    # Initialize repository to access data if needed
    data_repo = SQLAlchemyDataRepository()
    
    # Initialize Pulsar event bus
    pulsar_service_url = os.environ.get('PULSAR_SERVICE_URL', 'pulsar://localhost:6650')
    event_bus = PulsarEventBus(service_url=pulsar_service_url, client_id="processing-service")
    
    # Handler for DataIngested events
    def handle_data_ingested(event):
        print(f"Processing service received DataIngested event - ID: {event.data_id}, Partner: {event.partner_id}")
        
        # Process the data
        result = process_data(event.data_id, event.partner_id, event.timestamp)
        
        # Publish a DataProcessed event
        processed_event = DataProcessed(
            data_id=event.data_id,
            partner_id=event.partner_id,
            result=result
        )
        event_bus.publish(processed_event)
        print(f"Published DataProcessed event for data ID: {event.data_id}")
    
    # Subscribe to DataIngested events
    event_bus.subscribe(DataIngested, handle_data_ingested)
    
    print("Processing service is running. Press Ctrl+C to exit.")
    
    # Keep the service running until terminated
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up resources
        event_bus.close()
        print("Processing service has been shut down.")

if __name__ == "__main__":
    main() 
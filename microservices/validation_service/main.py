#!/usr/bin/env python
# microservices/validation_service/main.py
import os
import sys
import time
import signal
import json

# Add the root directory to the path so we can import from the main project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from infrastructure.event_bus import PulsarEventBus
from domain.events import DataIngested, DataValidated
from infrastructure.repositories_impl import SQLAlchemyDataRepository

# Flag to control the main loop
running = True

def signal_handler(sig, frame):
    """Handle termination signals"""
    global running
    print("Shutting down validation service...")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def validate_data(data_id, partner_id, data_repo):
    """
    Validate the data by retrieving it from the repository
    In a real application, this would perform actual validation on the data
    """
    print(f"Validating data: {data_id} from partner {partner_id}")
    
    # Get the data from the repository
    data = data_repo.get_by_id(data_id)
    if not data:
        return False, ["Data not found in repository"]
    
    # Simulate validation
    payload = data.payload.value
    errors = []
    
    # Example validation rules (customize based on your data structure)
    if isinstance(payload, dict):
        # Check for required fields
        if 'name' in payload and not payload['name']:
            errors.append("Name field is required")
        
        # Check for data types
        if 'age' in payload and not isinstance(payload['age'], (int, float)):
            errors.append("Age must be a number")
        
        # Check for value ranges
        if 'age' in payload and isinstance(payload['age'], (int, float)) and (payload['age'] < 0 or payload['age'] > 120):
            errors.append("Age must be between 0 and 120")
    else:
        errors.append("Payload must be a JSON object")
    
    # Return validation result
    is_valid = len(errors) == 0
    return is_valid, errors

def main():
    """Main function for the validation service"""
    print("Starting data validation service...")
    
    # Initialize repository to access data
    data_repo = SQLAlchemyDataRepository()
    
    # Initialize Pulsar event bus
    pulsar_service_url = os.environ.get('PULSAR_SERVICE_URL', 'pulsar://localhost:6650')
    event_bus = PulsarEventBus(service_url=pulsar_service_url, client_id="validation-service")
    
    # Handler for DataIngested events
    def handle_data_ingested(event):
        print(f"Validation service received DataIngested event - ID: {event.data_id}, Partner: {event.partner_id}")
        
        # Validate the data
        is_valid, errors = validate_data(event.data_id, event.partner_id, data_repo)
        
        # Publish a DataValidated event
        validated_event = DataValidated(
            data_id=event.data_id,
            partner_id=event.partner_id,
            is_valid=is_valid,
            validation_errors=errors
        )
        event_bus.publish(validated_event)
        
        validation_status = "valid" if is_valid else "invalid"
        print(f"Published DataValidated event for data ID: {event.data_id} - Status: {validation_status}")
        if not is_valid:
            print(f"Validation errors: {errors}")
    
    # Subscribe to DataIngested events
    event_bus.subscribe(DataIngested, handle_data_ingested)
    
    print("Validation service is running. Press Ctrl+C to exit.")
    
    # Keep the service running until terminated
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up resources
        event_bus.close()
        print("Validation service has been shut down.")

if __name__ == "__main__":
    main() 
#!/bin/bash
# Script to run all microservices locally for development

# Check if Python virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Please activate your Python virtual environment first."
    echo "Example: source venv/bin/activate"
    exit 1
fi

# Function to run a microservice in the background
run_service() {
    local service_name=$1
    local port=$2
    
    echo "Starting $service_name on port $port..."
    PORT=$port python microservices/$service_name/main.py &
    echo "$service_name started with PID $!"
}

# Create necessary directories if they don't exist
mkdir -p logs

# Kill any existing microservices
echo "Stopping any existing microservices..."
pkill -f "python microservices/.*/main.py" || true
sleep 2

# Start all microservices
run_service "ingestion_service" 5001
run_service "query_service" 5002
run_service "processing_service" 5003
run_service "validation_service" 5004

echo "All microservices are running. Press Ctrl+C to stop all."

# Wait for Ctrl+C
trap "echo 'Stopping all microservices...'; pkill -f 'python microservices/.*/main.py'" SIGINT SIGTERM
wait
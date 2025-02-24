from domain.seedwork import Command, CommandHandler
from domain.factories import IngestedDataFactory
from domain.repositories import DataRepository
from typing import Dict, Any


class IngestDataCommand(Command):
    """Command to ingest new data into the system"""
    
    def __init__(self, partner_id: str, payload: Dict[str, Any]):
        self.partner_id = partner_id
        self.payload = payload


class IngestDataCommandHandler(CommandHandler):
    """Handler for IngestDataCommand"""
    
    def __init__(self, repository: DataRepository, event_bus):
        self.repository = repository
        self.event_bus = event_bus
        self.factory = IngestedDataFactory()
    
    def handle(self, command: IngestDataCommand):
        """Handle the IngestDataCommand"""
        # Create a new IngestedData entity using the factory
        data = self.factory.create(command.partner_id, command.payload)
        
        # Persist the entity
        self.repository.add(data)
        
        # Publish domain events
        for event in data.get_events():
            self.event_bus.publish(event)
        
        # Clear events to prevent duplicate publishing
        data.clear_events()
        
        return data
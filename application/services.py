
from domain.entities import IngestedData
from domain.repositories import DataRepository

class DataIngestionService:
    def __init__(self, repo: DataRepository, event_bus):
        self.repo = repo
        self.event_bus = event_bus

    def ingest_data(self, partner_id: str, payload: dict):        
        data = IngestedData(partner_id, payload)        
        self.repo.add(data)        
        for event in data.get_events():
            self.event_bus.publish(event)        
        data.clear_events()
        return data
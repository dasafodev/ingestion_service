# domain/entities.py
import uuid
from datetime import datetime
from .events import DataIngested

class IngestedData:
    def __init__(self, partner_id: str, payload: dict):
        self.id = str(uuid.uuid4())
        self.partner_id = partner_id
        self.payload = payload
        self.timestamp = datetime.utcnow()      
        self._events = []
        self._record_event(DataIngested(self.id, self.partner_id, self.timestamp))

    def _record_event(self, event):
        self._events.append(event)

    def get_events(self):
        return self._events

    def clear_events(self):
        self._events = []
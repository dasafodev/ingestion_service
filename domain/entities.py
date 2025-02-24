# domain/entities.py
from .seedwork import Entity, Aggregate
from .value_objects import Timestamp, PartnerId, Payload
from .events import DataIngested
from typing import Dict, Any


class IngestedData(Aggregate):
    """Aggregate root for ingested data"""
    
    def __init__(self, partner_id: PartnerId, payload: Payload, timestamp: Timestamp = None):
        super().__init__()
        self._partner_id = partner_id
        self._payload = payload
        self._timestamp = timestamp or Timestamp()
        self._record_event(DataIngested(self.id, self.partner_id.value, self.timestamp.value))
    
    @property
    def partner_id(self) -> PartnerId:
        return self._partner_id
    
    @property
    def payload(self) -> Payload:
        return self._payload
    
    @property
    def timestamp(self) -> Timestamp:
        return self._timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary representation"""
        return {
            "id": self.id,
            "partner_id": self.partner_id.value,
            "payload": self.payload.value,
            "timestamp": self.timestamp.value.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IngestedData':
        """Create entity from dictionary representation"""
        from datetime import datetime
        
        entity = cls(
            partner_id=PartnerId(data["partner_id"]),
            payload=Payload(data["payload"]),
            timestamp=Timestamp(datetime.fromisoformat(data["timestamp"]))
        )
        entity.id = data["id"]
        return entity
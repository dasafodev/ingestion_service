# domain/factories.py
from .seedwork import Factory
from .entities import IngestedData
from .value_objects import PartnerId, Payload, Timestamp
from typing import Dict, Any


class IngestedDataFactory(Factory):
    """Factory for creating IngestedData entities"""
    
    def create(self, partner_id: str, payload: Dict[str, Any], timestamp=None) -> IngestedData:
        """Create a new IngestedData entity"""
        return IngestedData(
            partner_id=PartnerId(partner_id),
            payload=Payload(payload),
            timestamp=Timestamp(timestamp) if timestamp else None
        ) 
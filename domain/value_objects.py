from datetime import datetime
from .seedwork import ValueObject
from typing import Dict, Any


class Timestamp(ValueObject):
    """Value object representing a timestamp"""
    
    def __init__(self, value: datetime = None):
        self.value = value or datetime.utcnow()
    
    def __eq__(self, other):
        if not isinstance(other, Timestamp):
            return False
        return self.value == other.value


class PartnerId(ValueObject):
    """Value object representing a partner identifier"""
    
    def __init__(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Partner ID must be a non-empty string")
        self.value = value
    
    def __eq__(self, other):
        if not isinstance(other, PartnerId):
            return False
        return self.value == other.value


class Payload(ValueObject):
    """Value object representing the data payload"""
    
    def __init__(self, value: Dict[str, Any]):
        if not isinstance(value, dict):
            raise ValueError("Payload must be a dictionary")
        self.value = value
    
    def __eq__(self, other):
        if not isinstance(other, Payload):
            return False
        return self.value == other.value 
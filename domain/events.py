from .seedwork import DomainEvent
from datetime import datetime


class DataIngested(DomainEvent):
    """Event triggered when new data is ingested into the system"""
    
    def __init__(self, data_id: str, partner_id: str, timestamp: datetime):
        super().__init__()
        self.data_id = data_id
        self.partner_id = partner_id
        self.timestamp = timestamp


class DataProcessed(DomainEvent):
    """Event triggered when data has been processed"""
    
    def __init__(self, data_id: str, partner_id: str, result: dict):
        super().__init__()
        self.data_id = data_id
        self.partner_id = partner_id
        self.result = result


class DataValidated(DomainEvent):
    """Event triggered when data has been validated"""
    
    def __init__(self, data_id: str, partner_id: str, is_valid: bool, validation_errors=None):
        super().__init__()
        self.data_id = data_id
        self.partner_id = partner_id
        self.is_valid = is_valid
        self.validation_errors = validation_errors or []
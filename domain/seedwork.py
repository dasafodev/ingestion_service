# domain/seedwork.py
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any, Dict, Type


class Entity(ABC):
    """Base class for all domain entities"""
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self._events = []
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
    
    def _record_event(self, event):
        self._events.append(event)
    
    def get_events(self):
        return self._events
    
    def clear_events(self):
        self._events = []


class ValueObject(ABC):
    """Base class for all value objects"""
    
    @abstractmethod
    def __eq__(self, other):
        pass


class DomainEvent(ABC):
    """Base class for all domain events"""
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.occurred_on = datetime.utcnow()


class Repository(ABC):
    """Base interface for all repositories"""
    
    @abstractmethod
    def add(self, entity):
        pass
    
    @abstractmethod
    def update(self, entity):
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id):
        pass
    
    @abstractmethod
    def get_all(self):
        pass


class Aggregate(Entity):
    """Base class for all aggregates"""
    pass


class Factory(ABC):
    """Base interface for all factories"""
    
    @abstractmethod
    def create(self, *args, **kwargs):
        pass


class Service(ABC):
    """Base interface for all domain services"""
    pass


class Command(ABC):
    """Base class for all commands"""
    pass


class Query(ABC):
    """Base class for all queries"""
    pass


class CommandHandler(ABC):
    """Base interface for all command handlers"""
    
    @abstractmethod
    def handle(self, command):
        pass


class QueryHandler(ABC):
    """Base interface for all query handlers"""
    
    @abstractmethod
    def handle(self, query):
        pass


class EventBus(ABC):
    """Base interface for event bus"""
    
    @abstractmethod
    def publish(self, event):
        pass
    
    @abstractmethod
    def subscribe(self, event_type, handler):
        pass 
import threading
from domain.seedwork import EventBus, DomainEvent
from typing import Dict, List, Type, Callable, Any


class SimpleEventBus(EventBus):
    """Simple in-memory implementation of EventBus"""
    
    def __init__(self):
        self.subscribers: Dict[Type[DomainEvent], List[Callable]] = {}
    
    def subscribe(self, event_type: Type[DomainEvent], handler: Callable[[DomainEvent], Any]):
        """Subscribe a handler to a specific event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    def publish(self, event: DomainEvent):
        """Publish an event to all subscribers"""
        event_type = type(event)
        handlers = self.subscribers.get(event_type, [])
        for handler in handlers:
            # Run handlers in separate threads to avoid blocking
            threading.Thread(target=handler, args=(event,)).start()
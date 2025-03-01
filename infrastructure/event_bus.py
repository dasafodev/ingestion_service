import threading
import json
import uuid
import pulsar
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


class PulsarEventBus(EventBus):
    """Apache Pulsar implementation of EventBus"""
    
    def __init__(self, service_url="pulsar://localhost:6650", client_id=None):
        self.service_url = service_url
        self.client_id = client_id or f"producer-{uuid.uuid4()}"
        self.client = pulsar.Client(service_url)
        self.producers = {}
        self.consumers = {}
        self.subscribers = {}
        self.event_type_mapping = {}
    
    def _get_topic_name(self, event_type):
        """Convert event type to topic name"""
        return f"persistent://public/default/{event_type.__name__}"
    
    def _serialize_event(self, event):
        """Serialize event to JSON with type information"""
        event_dict = event.__dict__.copy()
        # Add type information
        event_dict['_event_type'] = event.__class__.__name__
        
        # Convert datetime objects to ISO format strings
        for key, value in event_dict.items():
            if hasattr(value, 'isoformat'):
                event_dict[key] = value.isoformat()
        
        return json.dumps(event_dict).encode('utf-8')
    
    def _get_producer(self, topic):
        """Get or create a producer for the topic"""
        if topic not in self.producers:
            self.producers[topic] = self.client.create_producer(topic)
        return self.producers[topic]
    
    def subscribe(self, event_type: Type[DomainEvent], handler: Callable[[DomainEvent], Any]):
        """Subscribe a handler to a specific event type"""
        topic = self._get_topic_name(event_type)
        
        # Store the mapping from event type name to class
        self.event_type_mapping[event_type.__name__] = event_type
        
        if topic not in self.subscribers:
            self.subscribers[topic] = []
            
            # Create a subscription name based on the service name
            subscription_name = f"{self.client_id}-{event_type.__name__}"
            
            # Create a consumer
            consumer = self.client.subscribe(
                topic,
                subscription_name,
                consumer_type=pulsar.ConsumerType.Shared
            )
            
            # Start a thread to listen for messages
            def message_listener():
                while True:
                    try:
                        msg = consumer.receive()
                        try:
                            # Deserialize the message
                            event_data = json.loads(msg.data().decode('utf-8'))
                            event_type_name = event_data.pop('_event_type', None)
                            
                            if event_type_name in self.event_type_mapping:
                                # Recreate the event object
                                event_class = self.event_type_mapping[event_type_name]
                                event = event_class.__new__(event_class)
                                event.__dict__.update(event_data)
                                
                                # Call all handlers
                                for handler in self.subscribers[topic]:
                                    threading.Thread(target=handler, args=(event,)).start()
                            
                            # Acknowledge the message
                            consumer.acknowledge(msg)
                        except Exception as e:
                            print(f"Error processing message: {e}")
                            consumer.negative_acknowledge(msg)
                    except Exception as e:
                        print(f"Error receiving message: {e}")
            
            # Start the listener thread
            threading.Thread(target=message_listener, daemon=True).start()
            self.consumers[topic] = consumer
        
        self.subscribers[topic].append(handler)
    
    def publish(self, event: DomainEvent):
        """Publish an event to Pulsar"""
        topic = self._get_topic_name(type(event))
        producer = self._get_producer(topic)
        
        # Serialize the event
        message = self._serialize_event(event)
        
        # Send the message
        producer.send(message)
    
    def close(self):
        """Close all producers and consumers"""
        for producer in self.producers.values():
            producer.close()
        
        for consumer in self.consumers.values():
            consumer.close()
        
        self.client.close()
import threading

class SimpleEventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, handler):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event):
        event_type = type(event)
        handlers = self.subscribers.get(event_type, [])        
        for handler in handlers:
            threading.Thread(target=handler, args=(event,)).start()
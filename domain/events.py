class DomainEvent:
    def __init__(self):
        self.ocurrido_en = None  

class DataIngested(DomainEvent):
    def __init__(self, data_id: str, partner_id: str, timestamp):
        super().__init__()
        self.data_id = data_id
        self.partner_id = partner_id
        self.timestamp = timestamp
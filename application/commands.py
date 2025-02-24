class IngestDataCommand:
    def __init__(self, partner_id: str, payload: dict):
        self.partner_id = partner_id
        self.payload = payload
from domain.entities import IngestedData
from domain.repositories import DataRepository

class InMemoryDataRepository(DataRepository):
    def __init__(self):
        self.data_store = {}

    def add(self, data: IngestedData):
        self.data_store[data.id] = data

    def get_by_id(self, data_id: str) -> IngestedData:
        return self.data_store.get(data_id)
    
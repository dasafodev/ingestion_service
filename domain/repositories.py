# domain/repositories.py
from abc import ABC, abstractmethod
from .entities import IngestedData

class DataRepository(ABC):
    @abstractmethod
    def add(self, data: IngestedData):
        pass

    @abstractmethod
    def get_by_id(self, data_id: str) -> IngestedData:
        pass

# domain/repositories.py
from .seedwork import Repository
from .entities import IngestedData
from typing import List, Optional


class DataRepository(Repository):
    """Repository interface for IngestedData entities"""
    
    def add(self, data: IngestedData) -> None:
        """Add a new IngestedData entity to the repository"""
        pass
    
    def update(self, data: IngestedData) -> None:
        """Update an existing IngestedData entity in the repository"""
        pass
    
    def get_by_id(self, data_id: str) -> Optional[IngestedData]:
        """Get an IngestedData entity by its ID"""
        pass
    
    def get_all(self) -> List[IngestedData]:
        """Get all IngestedData entities"""
        pass
    
    def get_by_partner_id(self, partner_id: str) -> List[IngestedData]:
        """Get all IngestedData entities for a specific partner"""
        pass

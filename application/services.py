from domain.repositories import DataRepository
from domain.entities import IngestedData
from .commands import IngestDataCommand, IngestDataCommandHandler
from .queries import GetDataByIdQuery, GetDataByIdQueryHandler
from typing import Optional, List


class DataIngestionService:
    """Service for data ingestion operations"""
    
    def __init__(self, repository: DataRepository, event_bus):
        self.repository = repository
        self.event_bus = event_bus
        self.command_handler = IngestDataCommandHandler(repository, event_bus)
        self.query_handler = GetDataByIdQueryHandler(repository)
    
    def ingest_data(self, partner_id: str, payload: dict) -> IngestedData:
        """Ingest new data into the system"""
        command = IngestDataCommand(partner_id, payload)
        return self.command_handler.handle(command)
    
    def get_data_by_id(self, data_id: str) -> Optional[IngestedData]:
        """Get data by ID"""
        query = GetDataByIdQuery(data_id)
        return self.query_handler.handle(query)


class QueryService:
    """Service for query operations"""
    
    def __init__(self, repository: DataRepository):
        self.repository = repository
    
    def get_data_by_id(self, data_id: str) -> Optional[IngestedData]:
        """Get data by ID"""
        handler = GetDataByIdQueryHandler(self.repository)
        query = GetDataByIdQuery(data_id)
        return handler.handle(query)
    
    def get_all_data(self) -> List[IngestedData]:
        """Get all data"""
        from .queries import GetAllDataQuery, GetAllDataQueryHandler
        handler = GetAllDataQueryHandler(self.repository)
        query = GetAllDataQuery()
        return handler.handle(query)
    
    def get_data_by_partner_id(self, partner_id: str) -> List[IngestedData]:
        """Get data by partner ID"""
        from .queries import GetDataByPartnerIdQuery, GetDataByPartnerIdQueryHandler
        handler = GetDataByPartnerIdQueryHandler(self.repository)
        query = GetDataByPartnerIdQuery(partner_id)
        return handler.handle(query)
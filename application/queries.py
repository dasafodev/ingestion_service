# application/queries.py
from domain.seedwork import Query, QueryHandler
from domain.repositories import DataRepository
from typing import List, Optional


class GetDataByIdQuery(Query):
    """Query to get data by ID"""
    
    def __init__(self, data_id: str):
        self.data_id = data_id


class GetDataByIdQueryHandler(QueryHandler):
    """Handler for GetDataByIdQuery"""
    
    def __init__(self, repository: DataRepository):
        self.repository = repository
    
    def handle(self, query: GetDataByIdQuery):
        """Handle the GetDataByIdQuery"""
        return self.repository.get_by_id(query.data_id)


class GetDataByPartnerIdQuery(Query):
    """Query to get data by partner ID"""
    
    def __init__(self, partner_id: str):
        self.partner_id = partner_id


class GetDataByPartnerIdQueryHandler(QueryHandler):
    """Handler for GetDataByPartnerIdQuery"""
    
    def __init__(self, repository: DataRepository):
        self.repository = repository
    
    def handle(self, query: GetDataByPartnerIdQuery):
        """Handle the GetDataByPartnerIdQuery"""
        return self.repository.get_by_partner_id(query.partner_id)


class GetAllDataQuery(Query):
    """Query to get all data"""
    pass


class GetAllDataQueryHandler(QueryHandler):
    """Handler for GetAllDataQuery"""
    
    def __init__(self, repository: DataRepository):
        self.repository = repository
    
    def handle(self, query: GetAllDataQuery):
        """Handle the GetAllDataQuery"""
        return self.repository.get_all() 
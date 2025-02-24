from domain.entities import IngestedData
from domain.repositories import DataRepository
from domain.value_objects import PartnerId, Payload, Timestamp
from .database import IngestedDataModel, SessionLocal
from typing import List, Optional
from datetime import datetime


class InMemoryDataRepository(DataRepository):
    """In-memory implementation of DataRepository"""
    
    def __init__(self):
        self.data_store = {}
    
    def add(self, data: IngestedData) -> None:
        self.data_store[data.id] = data
    
    def update(self, data: IngestedData) -> None:
        self.data_store[data.id] = data
    
    def get_by_id(self, data_id: str) -> Optional[IngestedData]:
        return self.data_store.get(data_id)
    
    def get_all(self) -> List[IngestedData]:
        return list(self.data_store.values())
    
    def get_by_partner_id(self, partner_id: str) -> List[IngestedData]:
        return [data for data in self.data_store.values() if data.partner_id.value == partner_id]


class SQLAlchemyDataRepository(DataRepository):
    """SQLAlchemy implementation of DataRepository"""
    
    def __init__(self):
        self.session_factory = SessionLocal
    
    def add(self, data: IngestedData) -> None:
        """Add a new IngestedData entity to the repository"""
        with self.session_factory() as session:
            db_data = IngestedDataModel(
                id=data.id,
                partner_id=data.partner_id.value,
                payload=data.payload.value,
                timestamp=data.timestamp.value
            )
            session.add(db_data)
            session.commit()
    
    def update(self, data: IngestedData) -> None:
        """Update an existing IngestedData entity in the repository"""
        with self.session_factory() as session:
            db_data = session.query(IngestedDataModel).filter(IngestedDataModel.id == data.id).first()
            if db_data:
                db_data.partner_id = data.partner_id.value
                db_data.payload = data.payload.value
                db_data.timestamp = data.timestamp.value
                session.commit()
    
    def get_by_id(self, data_id: str) -> Optional[IngestedData]:
        """Get an IngestedData entity by its ID"""
        with self.session_factory() as session:
            db_data = session.query(IngestedDataModel).filter(IngestedDataModel.id == data_id).first()
            if db_data:
                return IngestedData.from_dict({
                    "id": db_data.id,
                    "partner_id": db_data.partner_id,
                    "payload": db_data.payload,
                    "timestamp": db_data.timestamp.isoformat()
                })
            return None
    
    def get_all(self) -> List[IngestedData]:
        """Get all IngestedData entities"""
        with self.session_factory() as session:
            db_data_list = session.query(IngestedDataModel).all()
            return [
                IngestedData.from_dict({
                    "id": db_data.id,
                    "partner_id": db_data.partner_id,
                    "payload": db_data.payload,
                    "timestamp": db_data.timestamp.isoformat()
                })
                for db_data in db_data_list
            ]
    
    def get_by_partner_id(self, partner_id: str) -> List[IngestedData]:
        """Get all IngestedData entities for a specific partner"""
        with self.session_factory() as session:
            db_data_list = session.query(IngestedDataModel).filter(
                IngestedDataModel.partner_id == partner_id
            ).all()
            return [
                IngestedData.from_dict({
                    "id": db_data.id,
                    "partner_id": db_data.partner_id,
                    "payload": db_data.payload,
                    "timestamp": db_data.timestamp.isoformat()
                })
                for db_data in db_data_list
            ]
    
from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoCliente(EventoDominio):
    ...


@dataclass
class ProcessedImageCreada(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class ProcessedImageCancelada(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ProcessedImageGuardada(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ProcessedImageBorrar(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    fecha_actualizacion: datetime = None



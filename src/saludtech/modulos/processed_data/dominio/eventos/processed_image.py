from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoProcessedImage(EventoDominio):
    ...


@dataclass
class ProcessedImageCreada(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    url: str = None
    
@dataclass
class CreacionProcessedImageFallida(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    url: str = None

@dataclass
class ProcessedImageCancelada(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ProcessedImageGuardada(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ProcessedImageBorrada(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class GuardarProcessedImageFallida(EventoProcessedImage):
    id_processed_image: uuid.UUID = None
    fecha_actualizacion: datetime = None



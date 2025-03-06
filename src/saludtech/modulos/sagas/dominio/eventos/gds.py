from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoGDS(EventoDominio):
    ...

@dataclass
class ProcessedImageGDSConfirmada(EventoGDS):
    id_processed_image: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None

@dataclass
class ConfirmacionGDSRevertida(EventoGDS):
    id_processed_image: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None

@dataclass
class ConfirmacionFallida(EventoGDS):
    id_processed_image: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None
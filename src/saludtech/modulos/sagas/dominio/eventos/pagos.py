from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoPago(EventoDominio):
    ...

@dataclass
class ProcessedImagePagada(EventoPago):
    id_processed_image: uuid.UUID = None
    id_correlacion: str = None
    monto: float = None
    monto_vat: float = None
    fecha_actualizacion: datetime = None

@dataclass
class PagoFallido(EventoPago):
    id_processed_image: uuid.UUID = None
    id_correlacion: str = None
    monto: float = None
    monto_vat: float = None
    fecha_actualizacion: datetime = None

@dataclass
class PagoRevertido(EventoPago):
    id_processed_image: uuid.UUID = None
    id_correlacion: str = None
    monto: float = None
    monto_vat: float = None
    fecha_actualizacion: datetime = None
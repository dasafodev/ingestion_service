"""Objetos valor del dominio de processed_data

En este archivo usted encontrará los objetos valor del dominio de processed_data

"""

from __future__ import annotations

from dataclasses import dataclass, field
from saludtech.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class CodigoIATA(Codigo):
    ...

@dataclass(frozen=True)
class CodigoICAO(Codigo):
    ...

@dataclass(frozen=True)
class NombreAero():
    nombre: str

class TipoProcessedData(Enum):
    IMAGEN = "Imagen"

class EstadoProcessedImage(str, Enum):
    GUARDADA = "Guardada"
    PENDIENTE = "Pendiente"
    CANCELADA = "Cancelada"
    BORRADA = "Borrada"
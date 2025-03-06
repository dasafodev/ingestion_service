from dataclasses import dataclass, field
from saludtech.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class ProcessedImageDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    url: str = field(default_factory=str)
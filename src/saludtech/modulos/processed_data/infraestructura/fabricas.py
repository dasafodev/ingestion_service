""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de processed_data

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de processed_data

"""

from dataclasses import dataclass, field
from saludtech.seedwork.dominio.fabricas import Fabrica
from saludtech.seedwork.dominio.repositorios import Repositorio
from saludtech.seedwork.infraestructura.vistas import Vista
from saludtech.modulos.processed_data.infraestructura.vistas import VistaProcessedImage
from saludtech.modulos.processed_data.dominio.entidades import ProcessedImage
from saludtech.modulos.processed_data.dominio.repositorios import RepositorioProveedores, RepositorioProcessedImages, RepositorioEventosProcessedImages
from .repositorios import RepositorioProcessedImagesSQLAlchemy, RepositorioProveedoresSQLAlchemy, RepositorioEventosProcessedImageSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioProcessedImages:
            return RepositorioProcessedImagesSQLAlchemy()
        elif obj == RepositorioProveedores:
            return RepositorioProveedoresSQLAlchemy()
        elif obj == RepositorioEventosProcessedImages:
            return RepositorioEventosProcessedImageSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')

@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == ProcessedImage:
            return VistaProcessedImage()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')
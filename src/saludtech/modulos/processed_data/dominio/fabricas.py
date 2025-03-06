""" Fábricas para la creación de objetos del dominio de processed_data

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de processed_data

"""

from .entidades import ProcessedImage
from .reglas import MinimoUnItinerario, RutaValida
from .excepciones import TipoObjetoNoExisteEnDominioProcessedDatasExcepcion
from saludtech.seedwork.dominio.repositorios import Mapeador, Repositorio
from saludtech.seedwork.dominio.fabricas import Fabrica
from saludtech.seedwork.dominio.entidades import Entidad
from saludtech.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaProcessedImage(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            processed_image: ProcessedImage = mapeador.dto_a_entidad(obj)

            self.validar_regla(UrlValida(processed_image.url))
            
            return processed_image

@dataclass
class FabricaProcessedDatas(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == ProcessedImage.__class__:
            fabrica_processed_image = _FabricaProcessedImage()
            return fabrica_processed_image.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioProcessedDatasExcepcion()


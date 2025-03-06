""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de processed_data

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de processed_data

"""

from saludtech.config.db import db
from saludtech.modulos.processed_data.dominio.repositorios import RepositorioProcessedImages, RepositorioProveedores, RepositorioEventosProcessedImages
#from saludtech.modulos.processed_data.dominio.objetos_valor import NombreAero, Odo, Leg, Segmento, Itinerario, CodigoIATA
from saludtech.modulos.processed_data.dominio.entidades import ProcessedImage
from saludtech.modulos.processed_data.dominio.fabricas import FabricaProcessedDatas
from .dto import ProcessedImage as ProcessedImageDTO
from .dto import EventosProcessedImage
from .mapeadores import MapeadorProcessedImage, MapadeadorEventosProcessedImage
from uuid import UUID
from pulsar.schema import *

class RepositorioProcessedImagesSQLAlchemy(RepositorioProcessedImages):

    def __init__(self):
        self._fabrica_processed_data: FabricaProcessedDatas = FabricaProcessedDatas()

    @property
    def fabrica_processed_data(self):
        return self._fabrica_processed_data

    def obtener_por_id(self, id: UUID) -> ProcessedImage:
        processed_image_dto = db.session.query(ProcessedImageDTO).filter_by(id=str(id)).one()
        return self.fabrica_processed_data.crear_objeto(processed_image_dto, MapeadorProcessedImage())

    def obtener_todos(self) -> list[ProcessedImage]:
        # TODO
        raise NotImplementedError

    def agregar(self, processed_image: ProcessedImage):
        processed_image_dto = self.fabrica_processed_data.crear_objeto(processed_image, MapeadorProcessedImage())

        db.session.add(processed_image_dto)

    def actualizar(self, processed_image: ProcessedImage):
        # TODO
        raise NotImplementedError

    def eliminar(self, processed_image_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosProcessedImageSQLAlchemy(RepositorioEventosProcessedImages):

    def __init__(self):
        self._fabrica_processed_data: FabricaProcessedDatas = FabricaProcessedDatas()

    @property
    def fabrica_processed_data(self):
        return self._fabrica_processed_data

    def obtener_por_id(self, id: UUID) -> ProcessedImage:
        processed_image_dto = db.session.query(ProcessedImageDTO).filter_by(id=str(id)).one()
        return self.fabrica_processed_data.crear_objeto(processed_image_dto, MapadeadorEventosProcessedImage())

    def obtener_todos(self) -> list[ProcessedImage]:
        raise NotImplementedError

    def agregar(self, evento):
        processed_image_evento = self.fabrica_processed_data.crear_objeto(evento, MapadeadorEventosProcessedImage())

        parser_payload = JsonSchema(processed_image_evento.data.__class__)
        json_str = parser_payload.encode(processed_image_evento.data)

        evento_dto = EventosProcessedImage()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_processed_image)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(processed_image_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(processed_image_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, processed_image: ProcessedImage):
        raise NotImplementedError

    def eliminar(self, processed_image_id: UUID):
        raise NotImplementedError

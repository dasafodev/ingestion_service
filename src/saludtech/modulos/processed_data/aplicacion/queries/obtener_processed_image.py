from saludtech.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from saludtech.seedwork.aplicacion.queries import ejecutar_query as query
from saludtech.modulos.processed_data.infraestructura.repositorios import RepositorioProcessedImages
from saludtech.modulos.processed_data.dominio.entidades import ProcessedImage
from dataclasses import dataclass
from .base import ProcessedImageQueryBaseHandler
from saludtech.modulos.processed_data.aplicacion.mapeadores import MapeadorProcessedImage
import uuid

@dataclass
class ObtenerProcessedImage(Query):
    id: str

class ObtenerProcessedImageHandler(ProcessedImageQueryBaseHandler):

    def handle(self, query: ObtenerProcessedImage) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(ProcessedImage)
        processed_image =  self.fabrica_processed_data.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorProcessedImage())
        return QueryResultado(resultado=processed_image)

@query.register(ObtenerProcessedImage)
def ejecutar_query_obtener_processed_image(query: ObtenerProcessedImage):
    handler = ObtenerProcessedImageHandler()
    return handler.handle(query)
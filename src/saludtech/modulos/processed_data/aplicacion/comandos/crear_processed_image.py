from saludtech.seedwork.aplicacion.comandos import Comando
from saludtech.modulos.processed_data.aplicacion.dto import ProcessedImageDTO
from .base import CrearProcessedImageBaseHandler
from dataclasses import dataclass, field
from saludtech.seedwork.aplicacion.comandos import ejecutar_commando as comando

from saludtech.modulos.processed_data.dominio.entidades import ProcessedImage
from saludtech.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from saludtech.modulos.processed_data.aplicacion.mapeadores import MapeadorProcessedImage
from saludtech.modulos.processed_data.infraestructura.repositorios import RepositorioProcessedImages, RepositorioEventosProcessedImages

@dataclass
class CrearProcessedImage(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    url: str

class CrearProcessedImageHandler(CrearProcessedImageBaseHandler):
    
    def handle(self, comando: CrearProcessedImage):
        processed_image_dto = ProcessedImageDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   url=comando.url)

        processed_image: ProcessedImage = self.fabrica_processed_data.crear_objeto(processed_image_dto, MapeadorProcessedImage())
        processed_image.crear_processed_image(processed_image)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProcessedImages)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosProcessedImages)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, processed_image, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(CrearProcessedImage)
def ejecutar_comando_crear_processed_image(comando: CrearProcessedImage):
    handler = CrearProcessedImageHandler()
    handler.handle(comando)
    
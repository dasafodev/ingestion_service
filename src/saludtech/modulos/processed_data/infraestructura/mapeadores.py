""" Mapeadores para la capa de infrastructura del dominio de processed_data

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from saludtech.seedwork.dominio.repositorios import Mapeador
from saludtech.seedwork.infraestructura.utils import unix_time_millis
from saludtech.modulos.processed_data.dominio.objetos_valor import NombreAero, Odo, Leg, Segmento, Itinerario, CodigoIATA
from saludtech.modulos.processed_data.dominio.entidades import Proveedor, Aeropuerto, ProcessedImage
from saludtech.modulos.processed_data.dominio.eventos.processed_images import ProcessedImageAprobada, ProcessedImageCancelada, ProcessedImageAprobada, ProcessedImagePagada, ProcessedImageCreada, EventoProcessedImage

from .dto import ProcessedImage as ProcessedImageDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosProcessedImage(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            ProcessedImageCreada: self._entidad_a_processed_image_creada,
            ProcessedImageGuardada: self._entidad_a_processed_image_guardada,
            ProcessedImageCancelada: self._entidad_a_processed_image_cancelada,
            ProcessedImageBorrada: self._entidad_a_processed_image_borrada
        }

    def obtener_tipo(self) -> type:
        return EventoProcessedImage.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_processed_image_creada(self, entidad: ProcessedImageCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import ProcessedImageCreadaPayload, EventoProcessedImageCreada

            payload = ProcessedImageCreadaPayload(
                id_processed_image=str(evento.id_processed_image), 
                id_cliente=str(evento.id_cliente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoProcessedImageCreada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'ProcessedImageCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'saludtech'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_processed_image_guardada(self, entidad: ProcessedImageGuardada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_processed_image_cancelada(self, entidad: ProcessedImageCancelada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_processed_image_borrada(self, entidad: ProcessedImageBorrada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entidad_a_dto(self, entidad: EventoProcessedImage, version=LATEST_VERSION) -> ProcessedImageDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: ProcessedImageDTO, version=LATEST_VERSION) -> ProcessedImage:
        raise NotImplementedError


class MapeadorProcessedImage(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return ProcessedImage.__class__

    def entidad_a_dto(self, entidad: ProcessedImage) -> ProcessedImageDTO:
        
        processed_image_dto = ProcessedImageDTO()
        processed_image_dto.fecha_creacion = entidad.fecha_creacion
        processed_image_dto.fecha_actualizacion = entidad.fecha_actualizacion
        processed_image_dto.id = str(entidad.id)

        processed_image_dto.url = str(entidad.url)

        return processed_image_dto

    def dto_a_entidad(self, dto: ProcessedImageDTO) -> ProcessedImage:
        processed_image = ProcessedImage(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        processed_image.url = dto.url

        return processed_image
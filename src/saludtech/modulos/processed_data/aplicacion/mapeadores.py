from saludtech.seedwork.aplicacion.dto import Mapeador as AppMap
from saludtech.seedwork.dominio.repositorios import Mapeador as RepMap
from saludtech.modulos.processed_data.dominio.entidades import ProcessedImage
#from saludtech.modulos.processed_data.dominio.objetos_valor import Itinerario, Odo, Segmento, Leg
from .dto import ProcessedImageDTO

from datetime import datetime

class MapeadorProcessedImageDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ProcessedImageDTO:
        processed_image_dto = ProcessedImageDTO()

        url = externo.get('url')
        processed_image_dto.url = url

        return processed_image_dto

    def dto_a_externo(self, dto: ProcessedImageDTO) -> dict:
        return dto.__dict__

class MapeadorProcessedImage(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_itinerario(self, itinerario_dto: ItinerarioDTO) -> Itinerario:
        odos = list()

        for odo_dto in itinerario_dto.odos:
            segmentos = list()
            for seg_dto in odo_dto.segmentos:
                
                legs = list()

                for leg_dto in seg_dto.legs:
                    destino = Aeropuerto(codigo=leg_dto.destino.get('codigo'), nombre=leg_dto.destino.get('nombre'))
                    origen = Aeropuerto(codigo=leg_dto.origen.get('codigo'), nombre=leg_dto.origen.get('nombre'))
                    fecha_salida = datetime.strptime(leg_dto.fecha_salida, self._FORMATO_FECHA)
                    fecha_llegada = datetime.strptime(leg_dto.fecha_llegada, self._FORMATO_FECHA)

                    leg: Leg = Leg(fecha_salida, fecha_llegada, origen, destino)

                    legs.append(leg)

                segmentos.append(Segmento(legs))
            
            odos.append(Odo(segmentos))

        return Itinerario(odos)

    def obtener_tipo(self) -> type:
        return ProcessedImage.__class__

    def locacion_a_dict(self, locacion):
        if not locacion:
            return dict(codigo=None, nombre=None, fecha_actualizacion=None, fecha_creacion=None)
        
        return dict(
                    codigo=locacion.codigo
                ,   nombre=locacion.nombre
                ,   fecha_actualizacion=locacion.fecha_actualizacion.strftime(self._FORMATO_FECHA)
                ,   fecha_creacion=locacion.fecha_creacion.strftime(self._FORMATO_FECHA)
        )
        

    def entidad_a_dto(self, entidad: ProcessedImage) -> ProcessedImageDTO:
        
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        url = str(entidad.url)

        return ProcessedImageDTO(fecha_creacion, fecha_actualizacion, _id, itinerarios)

    def dto_a_entidad(self, dto: ProcessedImageDTO) -> ProcessedImage:
        processed_image = ProcessedImage()
        processed_image.url = dto.url

        return processed_image




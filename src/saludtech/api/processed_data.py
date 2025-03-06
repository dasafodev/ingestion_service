import saludtech.seedwork.presentacion.api as api
import json
from saludtech.modulos.processed_data.aplicacion.dto import ProcessedImageDTO
from saludtech.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from saludtech.modulos.processed_data.aplicacion.mapeadores import MapeadorProcessedImageDTOJson
from saludtech.modulos.processed_data.aplicacion.comandos.crear_processed_image import CrearProcessedImage
from saludtech.modulos.processed_data.aplicacion.queries.obtener_processed_image import ObtenerProcessedImage
from saludtech.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('processed_data', '/processed_data')

@bp.route('/processed_image', methods=('POST',))
def procesar_imagenes_usando_comando():
    try:
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'

        processed_image_dict = request.json

        map_processed_image = MapeadorProcessedImageDTOJson()
        processed_image_dto = map_processed_image.externo_a_dto(processed_image_dict)

        comando = CrearProcessedImage(processed_image_dto.fecha_creacion, processed_image_dto.fecha_actualizacion, processed_image_dto.id, processed_image_dto.itinerarios)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/processed_image', methods=('GET',))
@bp.route('/processed_image/<id>', methods=('GET',))
def dar_imagen_procesada_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerProcessedImage(id))
        map_processed_image = MapeadorProcessedImageDTOJson()
        
        return map_processed_image.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]
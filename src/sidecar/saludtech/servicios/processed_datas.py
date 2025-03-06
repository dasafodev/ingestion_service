import json
import requests
import datetime
import os

from saludtech.pb2py.processed_datas_pb2 import ProcessedImage, RespuestaProcessedImage
from saludtech.pb2py.processed_datas_pb2_grpc import ProcessedDatasServicer
from saludtech.utils import dict_a_proto_itinerarios

from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class ProcessedDatas(ProcessedDatasServicer):
    HOSTNAME_ENV: str = 'saludtech_ADDRESS'
    REST_API_HOST: str = f'http://{os.getenv(HOSTNAME_ENV, default="localhost")}:5000'
    REST_API_ENDPOINT: str = '/processed_datas/processed_image'

    def CrearProcessedImage(self, request, context):
        dict_obj = MessageToDict(request, preserving_proto_field_name=True)

        r = requests.post(f'{self.REST_API_HOST}{self.REST_API_ENDPOINT}', json=dict_obj)
        if r.status_code == 200:
            respuesta = json.loads(r.text)

            fecha_creacion_dt = datetime.datetime.strptime(respuesta['fecha_creacion'], TIMESTAMP_FORMAT)
            fecha_creacion = Timestamp()
            fecha_creacion.FromDatetime(fecha_creacion_dt)

            fecha_actualizacion_dt = datetime.datetime.strptime(respuesta['fecha_actualizacion'], TIMESTAMP_FORMAT)
            fecha_actualizacion = Timestamp()
            fecha_actualizacion.FromDatetime(fecha_actualizacion_dt)

            # Transformamos en 
            url = respuesta.get('url',"")


            processed_image =  ProcessedImage(id=respuesta.get('id'), 
                url=url, 
                fecha_actualizacion=fecha_actualizacion, 
                fecha_creacion=fecha_creacion)

            return RespuestaProcessedImage(mensaje='OK', processed_image=processed_image)
        else:
            return RespuestaProcessedImage(mensaje=f'Error: {r.status_code}')

    def ConsultarProcessedImage(self, request, context):
        # TODO Complete esta funcionalidad
        raise NotImplementedError
from __future__ import print_function

from google.protobuf.timestamp_pb2 import Timestamp
from saludtech.pb2py import processed_datas_pb2
from saludtech.pb2py import processed_datas_pb2_grpc
from saludtech.utils import dict_a_proto_itinerarios

import logging
import grpc
import datetime
import os
import json


def importar_comando_processed_image(json_file):
    json_dict = json.load(json_file)

    # Transformamos en 
    legs = json_dict['itinerarios'][0]['odos'][0]['segmentos'][0]['legs']

    TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    for leg in legs:
        leg['fecha_salida'] = datetime.datetime.strptime(leg['fecha_salida'], TIMESTAMP_FORMAT)
        leg['fecha_llegada'] = datetime.datetime.now()

    return json_dict

def dict_a_proto_processed_image(dict_processed_image):
    itinerarios = dict_a_proto_itinerarios(dict_processed_image.get('itinerarios', []))
    return processed_datas_pb2.ProcessedImage(id=dict_processed_image.get('id'), itinerarios=itinerarios)

def run():

    print("Crear una processed_image")
    with grpc.insecure_channel('localhost:50051') as channel:
        json_file = open(f'{os.path.dirname(__file__)}/mensajes/crear_processed_image.json')
        json_dict = importar_comando_processed_image(json_file)
        processed_image = dict_a_proto_processed_image(json_dict)


        stub = processed_datas_pb2_grpc.ProcessedDatasStub(channel)
        response = stub.CrearProcessedImage(processed_image)
    print("Greeter client received: " + response.mensaje)
    print(f'ProcessedImage: {response.processed_image}')


if __name__ == '__main__':
    logging.basicConfig()
    run()
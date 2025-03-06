import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from saludtech.modulos.processed_data.infraestructura.schema.v1.eventos import EventoProcessedImageCreada
from saludtech.modulos.processed_data.infraestructura.schema.v1.comandos import ComandoCrearProcessedImage


from saludtech.modulos.processed_data.infraestructura.proyecciones import ProyeccionProcessedImagesLista, ProyeccionProcessedImagesTotales
from saludtech.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from saludtech.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-processed_image', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='saludtech-sub-eventos', schema=AvroSchema(EventoProcessedImageCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionProcessedImagesTotales(datos.fecha_creacion, ProyeccionProcessedImagesTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionProcessedImagesLista(datos.id_processed_image, datos.id_cliente, datos.estado, datos.fecha_creacion, datos.fecha_creacion), app=app)
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-processed_image', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='saludtech-sub-comandos', schema=AvroSchema(ComandoCrearProcessedImage))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
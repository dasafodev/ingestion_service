from pulsar.schema import *
from .utils import time_millis
import uuid

class ProcessedImagePagada(Record):
    id = String(),
    id_correlacion = String(),
    processed_image_id = String()
    monto = Double()
    monto_vat = Double()
    fecha_creacion = Long()
 
class PagoRevertido(Record):
    id = String()
    id_correlacion = String()
    processed_image_id = String()
    fecha_actualizacion = Long()

class EventoPago(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoPago")
    datacontenttype = String()
    service_name = String(default="pagos.saludtech")
    processed_image_pagada = ProcessedImagePagada
    pago_revertido = PagoRevertido

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

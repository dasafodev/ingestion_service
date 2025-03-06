from pulsar.schema import *
from .utils import time_millis
import uuid

class ProcessedImageConfirmada(Record):
    id = String(),
    id_correlacion = String(),
    processed_image_id = String()
    fecha_confirmacion = Long()
 
class ConfirmacionRevertida(Record):
    id = String()
    id_correlacion = String()
    processed_image_id = String()
    fecha_actualizacion = Long()

class EventoConfirmacionGDS(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoPago")
    datacontenttype = String()
    service_name = String(default="pagos.saludtech")
    confirmacion_revertida = ConfirmacionRevertida
    processed_image_confirmada = ProcessedImageConfirmada

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

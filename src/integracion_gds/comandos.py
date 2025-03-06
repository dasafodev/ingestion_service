from pulsar.schema import *
from .utils import time_millis
import uuid

class ConfirmarProcessedImagePayload(Record):
    id_correlacion = String(),
    processed_image_id = String(),
 
class RevertirConfirmacionPayload(Record):
    id = String()
    id_correlacion = String()
    processed_image_id = String()

class ComandoConfirmarProcessedImage(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="ConfirmarProcessedImage")
    datacontenttype = String()
    service_name = String(default="gds.saludtech")
    data = ConfirmarProcessedImagePayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoRevertirConfirmacion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="RevertirConfirmacion")
    datacontenttype = String()
    service_name = String(default="gds.saludtech")
    data = RevertirConfirmacionPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from pulsar.schema import *
from .utils import time_millis
import uuid

class PagarProcessedImagePayload(Record):
    id_correlacion = String(),
    processed_image_id = String(),
    monto = Double()
    monto_vat = Double()
    fecha_creacion = Long()
 
class RevertirPagoPayload(Record):
    id = String()
    id_correlacion = String()
    processed_image_id = String()

class ComandoPagarProcessedImage(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="ComandoPagarProcessedImage")
    datacontenttype = String()
    service_name = String(default="pagos.saludtech")
    data = PagarProcessedImagePayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoRevertirPago(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="RevertirPagoProcessedImage")
    datacontenttype = String()
    service_name = String(default="pagos.saludtech")
    data = RevertirPagoPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

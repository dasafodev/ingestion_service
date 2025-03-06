from pulsar.schema import *
from dataclasses import dataclass, field
from saludtech.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearProcessedImagePayload(ComandoIntegracion):
    id_usuario = String()
    # TODO Cree los records para itinerarios

class ComandoCrearProcessedImage(ComandoIntegracion):
    data = ComandoCrearProcessedImagePayload()
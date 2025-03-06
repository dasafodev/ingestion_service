"""Entidades del dominio de processed_data

En este archivo usted encontrará las entidades del dominio de processed_data

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import saludtech.modulos.processed_data.dominio.objetos_valor as ov
from saludtech.modulos.processed_data.dominio.eventos.processed_images import ProcessedImageCreada, ProcessedImageGuardada, ProcessedImageCancelada, ProcessedImageBorrada
from saludtech.seedwork.dominio.entidades import Locacion, AgregacionRaiz, Entidad


@dataclass
class ProcessedImage(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoProcessedImage = field(default=ov.EstadoProcessedImage.PENDIENTE)
    url: str = field(default_factory=str)

    def crear_processed_image(self, processed_image: ProcessedImage):
        self.id_cliente = processed_image.id_cliente
        self.estado = processed_image.estado
        self.url = processed_image.url
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(ProcessedImageCreada(id_processed_image=self.id, id_cliente=self.id_cliente, estado=self.estado.name, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación

    def guardar_processed_image(self):
        self.estado = ov.EstadoProcessedImage.GUARDADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(ProcessedImageGuardada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación

    def cancelar_processed_image(self):
        self.estado = ov.EstadoProcessedImage.CANCELADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(ProcessedImageCancelada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
    
    def borrar_processed_image(self):
        self.estado = ov.EstadoProcessedImage.BORRADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(ProcessedImageBorrada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación

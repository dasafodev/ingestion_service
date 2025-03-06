from saludtech.modulos.processed_data.dominio.eventos.processed_images import ProcessedImageCreada, ProcessedImageCancelada, ProcessedImageAprobada, ProcessedImagePagada
from saludtech.seedwork.aplicacion.handlers import Handler
from saludtech.modulos.processed_data.infraestructura.despachadores import Despachador

class HandlerProcessedImageIntegracion(Handler):

    @staticmethod
    def handle_processed_image_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-processed_image')

    @staticmethod
    def handle_processed_image_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-processed_image')

    @staticmethod
    def handle_processed_image_guardada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-processed_image')

    @staticmethod
    def handle_processed_image_borrada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-processed_image')


    
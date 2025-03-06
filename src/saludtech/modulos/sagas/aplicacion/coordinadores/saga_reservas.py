from saludtech.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from saludtech.seedwork.aplicacion.comandos import Comando
from saludtech.seedwork.dominio.eventos import EventoDominio

#from saludtech.modulos.sagas.aplicacion.comandos.cliente import RegistrarUsuario, ValidarUsuario
#from saludtech.modulos.sagas.aplicacion.comandos.pagos import PagarProcessedImage, RevertirPago
from saludtech.modulos.sagas.aplicacion.comandos.gds import ConfirmarProcessedImage, RevertirConfirmacion
from saludtech.modulos.processed_data.aplicacion.comandos.crear_processed_image import CrearProcessedImage
from saludtech.modulos.processed_data.aplicacion.comandos.guardar_processed_image import GuardarProcessedImage
from saludtech.modulos.processed_data.aplicacion.comandos.cancelar_processed_image import CancelarProcessedImage
from saludtech.modulos.processed_data.dominio.eventos.processed_images import ProcessedImageCreada, ProcessedImageCancelada, ProcessedImageGuardada, CreacionProcessedImageFallida, GuardarProcessedImageFallida
#from saludtech.modulos.sagas.dominio.eventos.pagos import ProcessedImageBorrada, PagoRevertido
from saludtech.modulos.sagas.dominio.eventos.gds import ProcessedImageGDSConfirmada, ConfirmacionGDSRevertida, ConfirmacionFallida


class CoordinadorProcessedImages(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=CrearProcessedImage, evento=ProcessedImageCreada, error=CreacionProcessedImageFallida, compensacion=CancelarProcessedImage),
            Transaccion(index=2, comando=GuardarProcessedImage, evento=ProcessedImageGuardada, error=GuardarProcessedImageFallida, compensacion=GuardarProcessedImage),
           # Transaccion(index=2, comando=PagarProcessedImage, evento=ProcessedImagePagada, error=PagoFallido, compensacion=RevertirPago),
            #Transaccion(index=3, comando=ConfirmarProcessedImage, evento=ProcessedImageGDSConfirmada, error=ConfirmacionFallida, compensacion=ConfirmacionGDSRevertida),
            #Transaccion(index=4, comando=AprobarProcessedImage, evento=ProcessedImageAprobada, error=AprobacionProcessedImageFallida, compensacion=CancelarProcessedImage),
            Fin(index=5)
        ]

    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])
    
    def terminar():
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        # TODO Persistir estado en DB
        # Probablemente usted podría usar un repositorio para ello
        ...

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        # TODO Transforma un evento en la entrada de un comando
        # Por ejemplo si el evento que llega es ProcessedImageCreada y el tipo_comando es PagarProcessedImage
        # Debemos usar los atributos de ProcessedImageCreada para crear el comando PagarProcessedImage
        ...


# TODO Agregue un Listener/Handler para que se puedan redireccionar eventos de dominio
def oir_mensaje(mensaje):
    if isinstance(mensaje, EventoDominio):
        coordinador = CoordinadorProcessedImages()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")

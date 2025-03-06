from saludtech.seedwork.aplicacion.queries import QueryHandler
from saludtech.modulos.processed_data.infraestructura.fabricas import FabricaVista
from saludtech.modulos.processed_data.dominio.fabricas import FabricaProcessedDatas

class ProcessedImageQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_processed_data: FabricaProcessedDatas = FabricaProcessedDatas()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_processed_data(self):
        return self._fabrica_processed_data    
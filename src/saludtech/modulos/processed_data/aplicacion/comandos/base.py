from saludtech.seedwork.aplicacion.comandos import ComandoHandler
from saludtech.modulos.processed_data.infraestructura.fabricas import FabricaRepositorio
from saludtech.modulos.processed_data.dominio.fabricas import FabricaProcessedDatas

class CrearProcessedImageBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_processed_data: FabricaProcessedDatas = FabricaProcessedDatas()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_processed_data(self):
        return self._fabrica_processed_data    
    
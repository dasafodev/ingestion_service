from saludtech.seedwork.infraestructura.vistas import Vista
from saludtech.modulos.processed_data.dominio.entidades import ProcessedImage
from saludtech.config.db import db
from .dto import ProcessedImage as ProcessedImageDTO

class VistaProcessedImage(Vista):
    def obtener_por(id=None, estado=None, id_cliente=None, **kwargs) -> [ProcessedImage]:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)
            
        # TODO Convierta ProcessedImageDTO a ProcessedImage y valide que la consulta es correcta
        return db.session.query(ProcessedImageDTO).filter_by(**params)

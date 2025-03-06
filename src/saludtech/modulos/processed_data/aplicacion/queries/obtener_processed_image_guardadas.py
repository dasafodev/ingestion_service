from saludtech.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerProcessedImagesGuardadas(Query):
    ...

class ObtenerProcessedImagesGuardadasHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...
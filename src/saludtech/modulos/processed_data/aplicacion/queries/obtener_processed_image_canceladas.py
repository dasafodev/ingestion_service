from saludtech.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerProcessedImagesCanceladas(Query):
    ...

class ObtenerProcessedImagesCanceladasHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...
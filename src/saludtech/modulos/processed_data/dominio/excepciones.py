""" Excepciones del dominio de processed_data

En este archivo usted encontrará los Excepciones relacionadas
al dominio de processed_data

"""

from saludtech.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioProcessedDatasExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de processed_data'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)
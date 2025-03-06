"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from saludtech.seedwork.dominio.reglas import ReglaNegocio
#from .objetos_valor import Ruta
#from .entidades import Pasajero
#from .objetos_valor import TipoPasajero, Itinerario


class UrlValida(ReglaNegocio):

    url: str

    def __init__(self, ruta, mensaje='La url propuesta es invalida'):
        super().__init__(mensaje)
        self.url = url

    def es_valido(self) -> bool:
        return bool(self.url and self.url.strip())
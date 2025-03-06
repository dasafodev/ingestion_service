""" Interfaces para los repositorios del dominio de processed_data

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de processed_data

"""

from abc import ABC
from saludtech.seedwork.dominio.repositorios import Repositorio

class RepositorioProcessedImages(Repositorio, ABC):
    ...

class RepositorioEventosProcessedImages(Repositorio, ABC):
    ...

class RepositorioProveedores(Repositorio, ABC):
    ...
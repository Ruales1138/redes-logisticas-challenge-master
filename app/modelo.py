# TODO: Agrega el código aquí
from abc import ABC, abstractmethod

from app.datos import distancias
from app.errores import DestinoInalcanzableError


class Transporte(ABC):
    def __init__(self, id_transporte: str, capacidad_maxima: int, ubicacion_actual: str):
        self.id_transporte: str = id_transporte
        self.capacidad_maxima: int = capacidad_maxima
        self.ubicacion_actual: str = ubicacion_actual

    @abstractmethod
    def estimar_tiempo_entrega(self, distancia_total: float) -> float:
        ...

    def calcular_ruta(self, destinos: list[str]):
        def calc_ruta():
            return False

        if not calc_ruta():
            raise DestinoInalcanzableError('')

        ruta = [self.ubicacion_actual]
        for destino in destinos:
            ruta.append(destino)

        return {"ruta": ruta,"distancia_total": 0}


    def generar_reporte(self, ruta: dict[str], archivo: str):
        pass

class Camion(Transporte):
    def __init__(self, velocidad_promedio: int, peajes: int, id_transporte: str, capacidad_maxima: int, ubicacion_actual: str):
        super.__init__(id_transporte, capacidad_maxima, ubicacion_actual)
        self.velocidad_promedio: int = velocidad_promedio
        self.peajes: int = peajes

    def estimar_tiempo_entrega(self):
        pass

class Avion(Transporte):
    def __init__(self, velocidad_promedio: int, horas_descanso: int):
        self.velocidad_promedio: int = velocidad_promedio
        self.horas_descanso: int = horas_descanso

    def estimar_tiempo_entrega(self):
        pass



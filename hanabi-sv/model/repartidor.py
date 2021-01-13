# pyre-strict

from typing import List, Tuple, Dict, Callable
from random import shuffle

class Repartidor():

    colores = ["Rojo", "Amarillo", "Verde", "Azul", "Blanco"]

    def __init__(self, funcion_mezcladora: Callable[[List[Tuple[int, str]]], None] = shuffle) -> None:
        self._mazo : List[Tuple[int, str]] = self.cartas_de_colores(1, 6) + self.cartas_de_colores(1, 4) + self.cartas_de_colores(1, 2)
        funcion_mezcladora(self._mazo)

    def repartir(self, cantidad: int) -> List[Tuple[int,str]]:
        repartidas = self._mazo[len(self._mazo) - cantidad:]    
        for _ in range(cantidad):
            self._mazo.pop()

        return repartidas

    def cartas_de_colores(self, baja: int, alta: int) -> List[Tuple[int, str]]:
        return [(numero, color) for numero in range(baja, alta+1) for color in self.colores]

    def mazo_vacio(self) -> bool:
        return len(self._mazo) == 0

    def cartas_restantes(self) -> int:
        return len(self._mazo)


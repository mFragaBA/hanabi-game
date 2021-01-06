# pyre-strict

from typing import List, Tuple, Dict
from random import shuffle

class Repartidor():

    colores = ["Rojo", "Amarillo", "Verde", "Azul", "Blanco"]

    def __init__(self, jugadores: List[str], nro_cartas_por_jugador: int):
        self._jugadores = jugadores
        self._tamanio_mano = nro_cartas_por_jugador

    def repartir(self) -> Dict[str, List[Tuple[int,str]]]:
        mazo = self.cartas_de_colores(1, 6) + self.cartas_de_colores(1, 4) + self.cartas_de_colores(1, 2)
        shuffle(mazo)

        cartas_por_jugador = {}
        for jugador in self._jugadores:
            cartas_por_jugador[jugador] = mazo[len(mazo)-self._tamanio_mano:]
            for _ in range(4):
                mazo.pop()

        return cartas_por_jugador


    def cartas_de_colores(self, baja: int, alta: int) -> List[Tuple[int, str]]:
        return [(numero, color) for numero in range(baja, alta+1) for color in self.colores]


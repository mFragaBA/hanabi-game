# pyre-strict
from typing import List, Dict, Tuple
from model.exceptions import *

from random import shuffle

class Juego():

    def __init__(self,
            jugadores: List[str] = [],
            vidas_iniciales: int = 3,
            ) -> None:
        self.validarJugadores(jugadores)
        self._jugadores = jugadores
        self._puntaje = 0
        self._vidas = vidas_iniciales
        self._cartas_por_jugador = repartir_cartas(jugadores)

    def validarJugadores(self, jugadores: List[str]) -> None:
        if len(jugadores) < 2:
            raise JuegoSinJugadoresSuficientesException()
        if len(jugadores) > 4:
            raise JuegoConDemasiadosJugadoresException()
        if any(jugadores.count(jugador) > 1 for jugador in jugadores):
            raise JuegoConJugadoresDuplicadosException()

    def jugadores(self):
        return self._jugadores

    def puntaje(self):
        return self._puntaje
    
    def vidas(self):
        return self._vidas

    def cartas_por_jugador(self):
        return self._cartas_por_jugador

def cartas_de_colores(baja: int, alta: int, colores: List[str]) -> List[Tuple[int, str]]:
    return [(numero, color) for numero in range(baja, alta+1) for color in colores]

def repartir_cartas(jugadores: List[str]) -> Dict[str, List[Tuple[int, str]]]:
    colores = ["Rojo", "Amarillo", "Verde", "Azul", "Blanco"]
    
    mazo = cartas_de_colores(1, 6, colores) + cartas_de_colores(1, 4, colores) + cartas_de_colores(1, 2, colores)
    shuffle(mazo)

    cartas_por_jugador = {}
    for jugador in jugadores:
        cartas_por_jugador[jugador] = mazo[len(mazo)-4:]
        for _ in range(4):
            mazo.pop()

    return cartas_por_jugador

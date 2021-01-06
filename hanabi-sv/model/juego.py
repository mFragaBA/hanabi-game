# pyre-strict
from typing import List, Dict, Tuple
from model.exceptions import *
from model.repartidor import Repartidor

class Juego():

    def __init__(self,
            jugadores: List[str] = [],
            vidas_iniciales: int = 3,
            ) -> None:
        self.validarJugadores(jugadores)
        self._jugadores = jugadores
        self._puntaje = 0
        self._vidas = vidas_iniciales
        self._cartas_por_jugador = Repartidor(jugadores, 5 if len(jugadores) < 4 else 4).repartir()

    def validarJugadores(self, jugadores: List[str]) -> None:
        if len(jugadores) < 2:
            raise JuegoSinJugadoresSuficientesException()
        if len(jugadores) > 4:
            raise JuegoConDemasiadosJugadoresException()
        if any(jugadores.count(jugador) > 1 for jugador in jugadores):
            raise JuegoConJugadoresDuplicadosException()

    def jugadores(self) -> List[str]:
        return self._jugadores

    def puntaje(self) -> int:
        return self._puntaje
    
    def vidas(self) -> int:
        return self._vidas

    def cartas_por_jugador(self) -> Dict[str, List[Tuple[int, str]]]:
        return self._cartas_por_jugador


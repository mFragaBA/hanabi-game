from model.exceptions import *

from typing import List, Dict, Any

class Lobby():

    def __init__(self, capacidad: int = 5) -> None:
        self._jugadores = []
        self._capacidad = capacidad

    def agregar_jugador(self, jugador: str) -> None:
        if jugador in self._jugadores:
            raise JugadorExistenteException()
        if self._capacidad == len(self._jugadores):
            raise LobbyCompletoException()

        self._jugadores.append(jugador)

    def sacar_jugador(self, jugador: str) -> None:
        if jugador not in self._jugadores:
            raise JugadorInexistenteException()
        self._jugadores.remove(jugador)

    def jugadores(self) -> List[str]:
        return self._jugadores

    def estado(self) -> Dict[str,Any]:
        return {
            'jugadores': self._jugadores
        }

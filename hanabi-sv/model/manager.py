# pyre-strict

from model.exceptions import *
from model.lobby import Lobby
from model.juego import Juego
from typing import List, Dict, Any

class Manager():

    def __init__(self) -> None:
        self._lobbies_por_jugador = {}
        self._lobbies_por_id = {}
        pass

    def listar_lobbies(self) -> List['Lobby']:
        return list(self._lobbies_por_id.keys())

    def crear_lobby(self, lobby_id: str) -> None:
        if lobby_id in self._lobbies_por_id:
            raise LobbyExistenteException()
        self._lobbies_por_id[lobby_id] = Lobby()

    def agregar_jugador(self, jugador: str, lobby_id: str) -> None:
        if jugador in self._lobbies_por_jugador:
            raise JugadorExistenteException()
        
        if lobby_id not in self._lobbies_por_id:
            self.crear_lobby(lobby_id)
        self._lobbies_por_jugador[jugador] = lobby_id

    def sala_de(self, jugador: str) -> str:
        return self._lobbies_por_jugador[jugador]


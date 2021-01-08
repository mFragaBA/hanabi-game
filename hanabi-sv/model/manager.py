# pyre-strict

from model.exceptions import *
from model.lobby import Lobby
from model.juego import Juego
from typing import List, Dict, Any

class Manager():

    def __init__(self) -> None:
        self._lobbies_por_jugador = {}
        self._lobbies_por_id = {}
        self._juegos_por_lobby_id = {}

    def listar_lobbies(self) -> List['Lobby']:
        return list(self._lobbies_por_id.keys())

    def crear_lobby(self, lobby_id: str) -> None:
        self._validar_nombre(lobby_id)
        self._validar_lobby_no_existente(lobby_id)

        self._lobbies_por_id[lobby_id] = Lobby()

    def agregar_jugador(self, jugador: str, lobby_id: str) -> None:
        self._validar_nombre(jugador)
        self._validar_jugador_no_existente(jugador)

        if lobby_id not in self._lobbies_por_id:
            self.crear_lobby(lobby_id)

        self._validar_partida_no_iniciada(lobby_id)

        self._lobbies_por_id[lobby_id].agregar_jugador(jugador)
        self._lobbies_por_jugador[jugador] = lobby_id

    def iniciar_juego_en(self, lobby_id: str) -> None:
        self._validar_lobby_existente(lobby_id)
        self._validar_partida_no_iniciada(lobby_id)

        jugadores = self._lobbies_por_id[lobby_id].jugadores()
        self._juegos_por_lobby_id[lobby_id] = Juego(jugadores, 3)

    def sala_de(self, jugador: str) -> str:
        return self._lobbies_por_jugador[jugador]

    def _validar_nombre(self, nombre: str) -> None:
        if not nombre or len(nombre) > 40:
            raise NombreInvalidoException()

    def _validar_jugador_no_existente(self, jugador: str) -> None:
        if jugador in self._lobbies_por_jugador:
            raise JugadorExistenteException()

    def _validar_lobby_no_existente(self, lobby_id: str) -> None:
        if lobby_id in self._lobbies_por_id:
            raise LobbyExistenteException()

    def _validar_lobby_existente(self, lobby_id: str) -> None:
        if lobby_id not in self._lobbies_por_id:
            raise LobbyInexistenteException()

    def _validar_partida_no_iniciada(self, lobby_id: str) -> None:
        if lobby_id in self._juegos_por_lobby_id:
            raise PartidaYaIniciadaException()


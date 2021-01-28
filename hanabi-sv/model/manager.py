# pyre-strict

from model.exceptions import *
from model.lobby import Lobby
from model.juego import Juego
from model.repartidor import Repartidor
from typing import List, Dict, Any, Callable, Tuple
from random import shuffle

class Manager():

    def __init__(self, mezcladora : Callable[[List[Tuple[int, str]]], None] = shuffle) -> None:
        self._lobbies_por_jugador : Dict[Tuple[str,str], str] = {}
        self._lobbies_por_id : Dict[str, 'Lobby'] = {}
        self._juegos_por_id : Dict[str, 'Juego'] = {}
        self._mezcladora = mezcladora

    def listar_lobbies(self) -> List[Dict[str,Any]]:
        return [ self._lobbies_por_id[lobby].lobby_info() for lobby in self._lobbies_por_id.keys() if lobby not in self._juegos_por_id ]

    def crear_lobby(self, lobby_id: str) -> None:
        self._validar_nombre(lobby_id)
        self._validar_lobby_no_existente(lobby_id)

        self._lobbies_por_id[lobby_id] = Lobby(lobby_id)

    def agregar_jugador(self, jugador: Tuple[str,str], lobby_id: str) -> None:
        self._validar_nombre(jugador[1])
        self._validar_jugador_no_existente(jugador)

        if lobby_id not in self._lobbies_por_id:
            self.crear_lobby(lobby_id)

        self._validar_partida_no_iniciada(lobby_id)

        self._lobbies_por_id[lobby_id].agregar_jugador(jugador[1])
        self._lobbies_por_jugador[jugador] = lobby_id

    def sacar_jugador(self, jugador: Tuple[str,str], lobby_id: str) -> None:
        self._validar_jugador_en_sala(jugador, lobby_id)
        self._validar_partida_no_iniciada(lobby_id)

        self._lobbies_por_id[lobby_id].sacar_jugador(jugador[1])
        del self._lobbies_por_jugador[jugador]

        if len(self._lobbies_por_id[lobby_id].jugadores()) == 0:
            del self._lobbies_por_id[lobby_id]


    def iniciar_juego_en(self, lobby_id: str) -> None:
        self._validar_lobby_existente(lobby_id)
        self._validar_partida_no_iniciada(lobby_id)

        jugadores = self._lobbies_por_id[lobby_id].jugadores()
        self._juegos_por_id[lobby_id] = Juego(jugadores, 3, Repartidor(self._mezcladora))

    def cortar_juego_en(self, lobby_id: str) -> None:
        self._validar_lobby_existente(lobby_id)
        self._validar_partida_iniciada(lobby_id)

        del self._juegos_por_id[lobby_id]

    def tomar_accion_en(self, lobby_id: str, accion: Dict[str, Any]) -> None:
        self._validar_lobby_existente(lobby_id)
        self._validar_partida_iniciada(lobby_id)

        self._juegos_por_id[lobby_id].tomar_accion(accion)

    def estado_en_partida_de(self, jugador: Tuple[str,str]) -> Dict[str, Any]:
        self._validar_jugador_existente(jugador)
        lobby_id = self._lobbies_por_jugador[jugador]
        self._validar_partida_iniciada(lobby_id)

        return self._juegos_por_id[lobby_id].estado_para(jugador[1])

    def sala_de(self, jugador: Tuple[str, str]) -> str:
        self._validar_jugador_existente(jugador)
        return self._lobbies_por_jugador[jugador]

    def estado_del_lobby_de(self, jugador: Tuple[str,str]) -> Dict[str, Any]:
        self._validar_jugador_existente(jugador)
        return self._lobbies_por_id[self.sala_de(jugador)].estado()

    def _validar_nombre(self, nombre: str) -> None:
        if not nombre or len(nombre) > 40:
            raise NombreInvalidoException()

    def _validar_jugador_no_existente(self, jugador: Tuple[str,str]) -> None:
        if jugador in self._lobbies_por_jugador:
            raise JugadorExistenteException()

    def _validar_jugador_existente(self, jugador: Tuple[str,str]) -> None:
        if jugador not in self._lobbies_por_jugador:
            raise JugadorInExistenteException()

    def _validar_lobby_no_existente(self, lobby_id: str) -> None:
        if lobby_id in self._lobbies_por_id:
            raise LobbyExistenteException()

    def _validar_lobby_existente(self, lobby_id: str) -> None:
        if lobby_id not in self._lobbies_por_id:
            raise LobbyInexistenteException()

    def _validar_partida_no_iniciada(self, lobby_id: str) -> None:
        if lobby_id in self._juegos_por_id:
            raise PartidaYaIniciadaException()

    def _validar_partida_iniciada(self, lobby_id: str) -> None:
        if lobby_id not in self._juegos_por_id:
            raise PartidaNoIniciadaException()

    def _validar_jugador_en_sala(self, jugador: Tuple[str,str], lobby_id: str) -> None:
        self._validar_jugador_existente(jugador)
        if self._lobbies_por_jugador[jugador] != lobby_id:
            raise JugadorInExistenteEnLobbyException()


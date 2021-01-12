# pyre-strict

import unittest

from typing import List, Dict, Any

from model.exceptions import *
from model.lobby import Lobby

class LobbyTest(unittest.TestCase):

    def test_lobby_se_crea_vacío(self) -> None:
        lobby = Lobby()

        self.assertEqual(0, len(lobby.jugadores()))

    def test_lobby_agrega_jugador(self) -> None:
        lobby = Lobby()

        lobby.agregar_jugador("Román")

        self.assertTrue("Román" in lobby.jugadores())
    
    def test_lobby_no_agrega_jugador_repetido(self) -> None:
        lobby = Lobby()

        lobby.agregar_jugador("Román")

        self.assertRaises(JugadorExistenteException,
                lobby.agregar_jugador, "Román")

    def test_lobby_respeta_capacidad(self) -> None:
        lobby = Lobby(2)
        lobby.agregar_jugador("Román")
        lobby.agregar_jugador("Ramón")

        self.assertRaises(LobbyCompletoException,
                lobby.agregar_jugador, "Pipo")

    def test_lobby_saca_jugadores(self) -> None:
        lobby = Lobby()
        lobby.agregar_jugador("Román")
        lobby.sacar_jugador("Román")

        self.assertEqual(0, len(lobby.jugadores()))

    def test_jugador_no_saca_jugadores_inexistentes(self) -> None:
        lobby = Lobby()
        
        self.assertRaises(JugadorInexistenteException,
                lobby.sacar_jugador, "Román")

        

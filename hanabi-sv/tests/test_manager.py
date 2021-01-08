# pyre-strict

import unittest
from model.manager import Manager
from model.exceptions import *

class ManagerTest(unittest.TestCase):
    
    def test_manager_inicia_sin_lobbies(self) -> None:
        manager = Manager()
        
        self.assertEqual([], manager.listar_lobbies())

    def test_manager_crea_un_lobby_nuevo_si_el_nombre_es_valido(self) -> None:
        manager = Manager()
        manager.crear_lobby("Amongas Volley Club")

        self.assertTrue("Amongas Volley Club" in manager.listar_lobbies())

    def test_manager_no_puede_crear_lobby_con_nombre_inválido(self) -> None:
        manager = Manager()

        self.assertRaises(NombreInvalidoException,
                manager.crear_lobby, "")
    
    def test_manager_no_puede_crear_lobby_con_nombre_largo(self) -> None:
        manager = Manager()

        self.assertRaises(NombreInvalidoException,
                manager.crear_lobby, "A" * 50)

    def test_manager_no_puedo_agregar_jugador_con_nombre_inválido(self) -> None:
        manager = Manager()
        self.assertRaises(NombreInvalidoException,
                manager.agregar_jugador, "Román" * 50, "Amongas Volley Club")


    def test_manager_no_puede_crear_lobby_ya_existente(self) -> None:
        manager = Manager()
        manager.crear_lobby("Amongas Volley Club")

        self.assertRaises(LobbyExistenteException,
                manager.crear_lobby, "Amongas Volley Club")

    def test_manager_unirse_con_usuario_a_lobby(self) -> None:
        manager = Manager()
        manager.crear_lobby("Amongas Volley Club")

        manager.agregar_jugador("Román", "Amongas Volley Club")

        self.assertEqual("Amongas Volley Club", manager.sala_de("Román"))

    def test_manager_unirse_a_lobby_inexistente_lo_tiene_que_crear(self) -> None:
        manager = Manager()

        manager.agregar_jugador("Román", "Amongas Volley Club")

        self.assertTrue("Amongas Volley Club" in manager.listar_lobbies())
        self.assertEqual("Amongas Volley Club", manager.sala_de("Román"))

    def test_manager_no_puede_unirse_con_usuario_repetido(self) -> None:
        manager = Manager()

        manager.agregar_jugador("Román", "Amongas Volley Club")

        self.assertRaises(JugadorExistenteException,
                manager.agregar_jugador, "Román", "Amongas Volley Club 2")
        self.assertFalse("Amongas Volley Club 2" in manager.listar_lobbies())

    def test_manager_pueden_haber_varios_lobbies(self) -> None:
        manager = Manager()

        manager.agregar_jugador("Román", "Amongas Volley Club")
        manager.agregar_jugador("Ramón", "Amongas Volley Club 2")

        self.assertEquals(["Amongas Volley Club", "Amongas Volley Club 2"], 
                manager.listar_lobbies())

    def test_manager_no_se_puede_unir_a_partida_iniciada(self) -> None:
        manager = Manager()
        manager.agregar_jugador("Román", "Amongas Volley Club")
        manager.agregar_jugador("Ramón", "Amongas Volley Club")
        manager.iniciar_juego_en("Amongas Volley Club")

        self.assertRaises(PartidaYaIniciadaException,
                manager.agregar_jugador, "Carlos", "Amongas Volley Club")

    def test_manager_no_se_puede_iniciar_una_partida_ya_iniciada(self) -> None:
        manager = Manager()
        manager.agregar_jugador("Román", "Amongas Volley Club")
        manager.agregar_jugador("Ramón", "Amongas Volley Club")
        manager.iniciar_juego_en("Amongas Volley Club")

        self.assertRaises(PartidaYaIniciadaException,
                manager.iniciar_juego_en, "Amongas Volley Club")

    def test_manager_no_se_puede_iniciar_una_partida_de_un_lobby_inexistente(self) -> None:
        manager = Manager()
        
        self.assertRaises(LobbyInexistenteException,
                manager.iniciar_juego_en, "Amongas Volley Club")


        


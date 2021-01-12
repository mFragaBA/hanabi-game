# pyre-strict

import unittest
from model.manager import Manager
from model.exceptions import *

from typing import List, Dict, Tuple

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

    def test_manager_iniciar_partida_la_deja_de_mostrar_al_listar(self) -> None:
        manager = Manager()
        manager.agregar_jugador("Román", "Amongas Volley Club")
        manager.agregar_jugador("Ramón", "Amongas Volley Club")
        manager.iniciar_juego_en("Amongas Volley Club")

        self.assertFalse("Amongas Volley Club" in manager.listar_lobbies())


    def test_manager_tomar_accion_en_partida(self) -> None:
        manager = Manager(mezclar_rojo_verde)

        manager.agregar_jugador("Román", "Amongas Volley Club")
        manager.agregar_jugador("Ramón", "Amongas Volley Club")
        manager.iniciar_juego_en("Amongas Volley Club")

        accion = {
                'jugador': "Román",
                'accion': 'DESCARTAR',
                'carta': 0
        }
        manager.tomar_accion_en("Amongas Volley Club", accion)

        self.assertEqual(
                {
                    'terminado': False,
                    'jugadores': ["Román", "Ramón"],
                    'turno_de': "Ramón",
                    'vidas': 3,
                    'pistas_restantes': 7,
                    'cartas_restantes': 9,
                    'cartas_de': {
                        'Román': [(i, "Verde") for i in range(2, 6)] + [(5, "Azul")],
                        'Ramón': [(i, "Rojo") for i in range(1,6)],
                    },
                    'pistas_de': {
                        'Román': [[], [], [], [], []],
                        'Ramón': [[], [], [], [], []]
                    },
                    'tablero': {
                        'Rojo': 0,
                        'Azul': 0,
                        'Amarillo': 0,
                        'Verde': 0,
                        'Blanco': 0
                    },
                    'puntaje': 0,
                    'descarte': {
                        'Rojo': [],
                        'Azul': [],
                        'Amarillo': [],
                        'Verde': [],
                        'Blanco': []
                    }
                },
                manager.estado_en("Amongas Volley Club"))
    
    def test_manager_no_se_puede_tomar_accion_en_lobby_inexistente(self) -> None:
        manager = Manager(mezclar_rojo_verde)

        accion = {
                'jugador': "Román",
                'accion': 'DESCARTAR',
                'carta': 0
        }

        self.assertRaises( LobbyInexistenteException,
                manager.tomar_accion_en, "Amongas Volley Club", accion)

    def test_manager_no_se_puede_tomar_accion_en_partida_no_iniciada(self) -> None:
        manager = Manager(mezclar_rojo_verde)

        manager.agregar_jugador("Román", "Amongas Volley Club")
        manager.agregar_jugador("Ramón", "Amongas Volley Club")

        accion = {
                'jugador': "Román",
                'accion': 'DESCARTAR',
                'carta': 0
        }

        self.assertRaises( PartidaNoIniciadaException,
                manager.tomar_accion_en, "Amongas Volley Club", accion)


    def test_manager_no_se_puede_pedir_estado_en_lobby_inexistente(self) -> None:
        manager = Manager(mezclar_rojo_verde)

        self.assertRaises( LobbyInexistenteException,
                manager.estado_en, "Amongas Volley Club")

    def test_manager_no_se_puede_pedir_estado_en_partida_no_iniciada(self) -> None:
        manager = Manager(mezclar_rojo_verde)

        manager.agregar_jugador("Román", "Amongas Volley Club")
        manager.agregar_jugador("Ramón", "Amongas Volley Club")

        self.assertRaises( PartidaNoIniciadaException,
                manager.estado_en, "Amongas Volley Club")


def mezclar_rojo_verde(mazo: List[Tuple[int, str]]) -> None:
    mazo.clear()
    mazo.append((1, "Amarillo"))
    mazo.append((2, "Amarillo"))
    mazo.append((3, "Amarillo"))
    mazo.append((4, "Amarillo"))
    mazo.append((5, "Amarillo"))
    mazo.append((1, "Azul"))
    mazo.append((2, "Azul"))
    mazo.append((3, "Azul"))
    mazo.append((4, "Azul"))
    mazo.append((5, "Azul"))
    mazo.append((1, "Rojo"))
    mazo.append((2, "Rojo"))
    mazo.append((3, "Rojo"))
    mazo.append((4, "Rojo"))
    mazo.append((5, "Rojo"))
    mazo.append((1, "Verde"))
    mazo.append((2, "Verde"))
    mazo.append((3, "Verde"))
    mazo.append((4, "Verde"))
    mazo.append((5, "Verde"))

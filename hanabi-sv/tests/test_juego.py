# pyre-strict

import unittest

from typing import Any, Dict, List, Generic, Optional, TypeVar

from model.exceptions import *
from model.juego import Juego

class JuegoTest(unittest.TestCase):

    def test_juego_inicia_en_blanco(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3)
        self.assertEqual(0, juego.puntaje())
        self.assertEqual(3, juego.vidas())
        self.assertEqual(jugadores, juego.jugadores())

    def test_juego_no_inicia_sin_jugadores(self) -> None:
        self.assertRaises(JuegoSinJugadoresSuficientesException,
                Juego, jugadores=[])

    def test_juego_no_inicia_con_un_jugador_solo(self) -> None:
        self.assertRaises(JuegoSinJugadoresSuficientesException,
                Juego, jugadores=["Román"])

    def test_juego_no_inicia_si_tiene_demasiados_jugadores(self) -> None:
        self.assertRaises(JuegoConDemasiadosJugadoresException,
                Juego, jugadores=["Zorro1", "Zorro2", "Zorro3", "Zorro4", "Zorro5"])

    def test_juego_con_duplicados_no_inicia(self) -> None:
        self.assertRaises(JuegoConJugadoresDuplicadosException,
                Juego, jugadores=["Zorro1", "Zorro8", "Zorro12", "Zorro1"])

    def test_juego_inicia_y_reparte_cartas_sin_repetir(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3)
        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(4, len(cartas_de["Román"])) 
        self.assertEqual(4, len(cartas_de["Ramón"])) 

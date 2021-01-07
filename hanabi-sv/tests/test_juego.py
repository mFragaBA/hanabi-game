# pyre-strict

import unittest

from typing import Any, Dict, List, Generic, Optional, TypeVar, Tuple

from model.exceptions import *
from model.juego import Juego
from model.repartidor import Repartidor

class JuegoTest(unittest.TestCase):

    def test_juego_inicia_en_blanco(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3)
        self.assertEqual(0, juego.puntaje())
        self.assertEqual(3, juego.vidas())
        self.assertEqual(7, juego.pistas_restantes())
        self.assertEqual(jugadores, juego.jugadores())
        self.assertEqual("Román", juego.turno_de())

    def test_juego_no_inicia_sin_jugadores(self) -> None:
        self.assertRaises(JuegoSinJugadoresSuficientesException,
                Juego, jugadores=[])

    def test_juego_no_inicia_con_un_jugador_solo(self) -> None:
        self.assertRaises(JuegoSinJugadoresSuficientesException,
                Juego, jugadores=["Román"])

    def test_juego_no_inicia_si_tiene_demasiados_jugadores(self) -> None:
        self.assertRaises(JuegoConDemasiadosJugadoresException,
                Juego, jugadores=["Zorro1", "Zorro2", "Zorro3", "Zorro4", "Zorro5", "Eres Un Id..."])

    def test_juego_con_duplicados_no_inicia(self) -> None:
        self.assertRaises(JuegoConJugadoresDuplicadosException,
                Juego, jugadores=["Zorro1", "Zorro8", "Zorro12", "Zorro1"])

    def test_juego_inicia_con_pocos_jugadores_y_reparte_cartas(self) -> None:
        jugadores = ["Román", "Ramón"]
        repartidor = self.repartidor_rojo_verde()
        juego = Juego(jugadores, 3, repartidor)
        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(5, len(cartas_de["Román"])) 
        self.assertEqual(5, len(cartas_de["Ramón"])) 
    
    def test_juego_inicia_con_muchos_jugadores_y_reparte_cartas(self) -> None:
        jugadores = ["Román", "Ramón", "Marón", "Morán"]
        repartidor = self.repartidor_rojo_verde()
        juego = Juego(jugadores, 3, repartidor)
        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(4, len(cartas_de["Román"])) 
        self.assertEqual(4, len(cartas_de["Ramón"])) 

    def test_juego_descartar_carta_recupera_otra_si_da_el_mazo(self) -> None:
        jugadores = ["Román", "Ramón"]
        repartidor = self.repartidor_rojo_verde()
        juego = Juego(jugadores, 3, repartidor)
        juego.descartar(0)

        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(5, len(cartas_de["Román"]))
        self.assertFalse((1, "Azul") in cartas_de["Román"])
        self.assertTrue((5, "Verde") in cartas_de["Román"])

    def test_juego_descartar_carta_no_recupera_con_mazo_vacío(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal))
        juego.descartar(0)

        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(4, len(cartas_de["Román"]))
        self.assertFalse((1, "Azul") in cartas_de["Román"])

    def test_juego_descartar_avanza_el_turno(self) -> None:
        jugadores = ["Román", "Ramón"]
        repartidor = self.repartidor_rojo_verde()
        juego = Juego(jugadores, 3, repartidor)
        
        juego.descartar(0)
        self.assertEqual("Ramón", juego.turno_de())
        
        juego.descartar(0)
        self.assertEqual("Román", juego.turno_de())

    def test_juego_descartar_tiene_que_ser_carta_de_la_mano(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 5)

        self.assertRaises(JuegoDescartaCartaFueraDeManoException,
                juego.descartar, 10)

    def test_juego_dar_pista_sobre_color(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        juego.dar_pista("Color", "Amarillo", "Ramón")

        pistas_de = juego.pistas_por_jugador()
        self.assertTrue(all("Amarillo" in pistas_de["Ramón"][i] for i in [0, 2, 4]))
        self.assertTrue(all(len(pistas_de["Ramón"][i]) == 0 for i in [1, 3]))
    
    def test_juego_dar_pista_sobre_numero(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        juego.dar_pista("Número", 1, "Ramón")

        pistas_de = juego.pistas_por_jugador()
        self.assertTrue(all("1" in pistas_de["Ramón"][i] for i in [0, 1]))
        self.assertTrue(all(len(pistas_de["Ramón"][i]) == 0 for i in [2, 3, 4]))

    def test_juego_tipo_de_pista_inválida(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        self.assertRaises(JuegoTipoDePistaInvalidoException,
                juego.dar_pista, "Sonamos", 1, "Ramón")
    
    def test_juego_pista_tiene_que_ser_de_alguien_en_partida(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        self.assertRaises(JuegoPistaSinDestinatarioException,
                juego.dar_pista, "Color", "Blanco", "Mirtha")

    def test_juego_cambia_el_turno_al_dar_pista(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        juego.dar_pista("Número", 1, "Ramón")
        
        self.assertEqual("Ramón", juego.turno_de())

    def test_juego_se_descartan_las_pistas_junto_con_la_carta(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        juego.dar_pista("Número", 1, "Ramón")
        juego.descartar(0)

        pistas_de = juego.pistas_por_jugador()
        self.assertTrue(len(pistas_de["Ramón"][-1]) == 0)

    def test_juego_no_se_agregan_pistas_si_no_se_agrega_carta(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal))
        juego.descartar(0)

        pistas_de = juego.pistas_por_jugador()

        self.assertEqual(4, len(pistas_de["Román"]))



    def mezclar_mazo_minimal(self, mazo: List[Tuple[int, str]]) -> None:
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

    def mezclar_mazo_minimal_mezcladito(self, mazo: List[Tuple[int, str]]) -> None:
        mazo.clear()
        mazo.append((1, "Amarillo"))
        mazo.append((1, "Azul"))
        mazo.append((2, "Amarillo"))
        mazo.append((2, "Azul"))
        mazo.append((3, "Amarillo"))
        mazo.append((3, "Azul"))
        mazo.append((4, "Amarillo"))
        mazo.append((4, "Azul"))
        mazo.append((5, "Amarillo"))
        mazo.append((5, "Azul"))
        
        

    def repartidor_rojo_verde(self) -> 'Repartidor':
        def mezclar(mazo: List[Tuple[int, str]]) -> None:
            self.mezclar_mazo_minimal(mazo)
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

        return Repartidor(mezclar)
        self.assertTrue((5, "Verde") in cartas_de["Román"])


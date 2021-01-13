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
        self.assertFalse(juego.terminado())

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
        juego = self.juego_default_2p()
        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(5, len(cartas_de["Román"])) 
        self.assertEqual(5, len(cartas_de["Ramón"])) 
    
    def test_juego_inicia_con_muchos_jugadores_y_reparte_cartas(self) -> None:
        juego = self.juego_default_4p()
        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(4, len(cartas_de["Román"])) 
        self.assertEqual(4, len(cartas_de["Ramón"])) 

    def test_juego_descartar_carta_recupera_otra_si_da_el_mazo(self) -> None:
        juego = self.juego_default_2p()
        juego.descartar(0)

        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(5, len(cartas_de["Román"]))
        self.assertFalse((1, "Verde") in cartas_de["Román"])
        self.assertTrue((5, "Azul") in cartas_de["Román"])

    def test_juego_descartar_carta_no_recupera_con_mazo_vacio(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal))
        juego.descartar(0)

        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(4, len(cartas_de["Román"]))
        self.assertFalse((1, "Azul") in cartas_de["Román"])

    def test_juego_descartar_avanza_el_turno(self) -> None:
        juego = self.juego_default_2p()
        
        juego.descartar(0)
        self.assertEqual("Ramón", juego.turno_de())
        
        juego.descartar(0)
        self.assertEqual("Román", juego.turno_de())

    def test_juego_descartar_tiene_que_ser_carta_de_la_mano(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 5)

        mano_ramon = [ carta for carta in juego.cartas_por_jugador()["Román"]]

        self.assertRaises(JuegoDescartaCartaFueraDeManoException,
                juego.descartar, 10)
        self.assertEqual(mano_ramon, juego.cartas_por_jugador()["Román"])
        self.assertEqual("Román", juego.turno_de())

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

    def test_juego_tipo_de_pista_invalida(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        self.assertRaises(JuegoTipoDePistaInvalidoException,
                juego.dar_pista, "Sonamos", 1, "Ramón")
        self.assertEqual(7, juego.pistas_restantes())
        self.assertEqual("Román", juego.turno_de())
    
    def test_juego_pista_tiene_que_ser_de_alguien_en_partida(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        self.assertRaises(JuegoPistaSinDestinatarioException,
                juego.dar_pista, "Color", "Blanco", "Mirtha")
        self.assertEqual(7, juego.pistas_restantes())
        self.assertEqual("Román", juego.turno_de())

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

    def test_juego_descartar_carta_recupera_pista(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        juego.dar_pista("Número", 1, "Ramón")
        self.assertEqual(6, juego.pistas_restantes())

        juego.descartar(0)
        self.assertEqual(7, juego.pistas_restantes())

    def test_juego_tienen_que_haber_pistas_disponibles(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        for _ in range(3):
            juego.dar_pista("Número", 1, "Ramón")
            juego.dar_pista("Número", 1, "Román")
        juego.dar_pista("Número", 1, "Ramón")

        self.assertRaises(JuegoSinPistasDisponiblesException,
                juego.dar_pista, "Número", 1, "Román")
        self.assertEqual(0, juego.pistas_restantes())
        self.assertEqual("Ramón", juego.turno_de())

    def test_juego_no_se_puede_dar_pista_a_si_mismo(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))
        
        self.assertRaises(JuegoPistaASiMismoException,
                juego.dar_pista, "Número", 1, "Román")
        self.assertEqual(7, juego.pistas_restantes())
        self.assertEqual("Román", juego.turno_de())


    def test_juego_bajar_remueve_carta_y_pista(self) -> None:
        juego = self.juego_default_2p()
        juego.bajar(0)

        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(5, len(cartas_de["Román"]))
        self.assertFalse((1, "Verde") in cartas_de["Román"])
        self.assertTrue((5, "Azul") in cartas_de["Román"])

    
    def test_juego_bajar_carta_no_recupera_con_mazo_vacio(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal))
        juego.bajar(0)

        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(4, len(cartas_de["Román"]))
        self.assertFalse((1, "Azul") in cartas_de["Román"])

    
    def test_juego_bajar_avanza_el_turno(self) -> None:
        juego = self.juego_default_2p()
        
        juego.bajar(0)
        self.assertEqual("Ramón", juego.turno_de())
        
        juego.bajar(0)
        self.assertEqual("Román", juego.turno_de())

    
    def test_juego_bajar_tiene_que_ser_carta_de_la_mano(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 5)

        mano_ramon = [ carta for carta in juego.cartas_por_jugador()["Román"]]

        self.assertRaises(JuegoDescartaCartaFueraDeManoException,
                juego.bajar, 10)

        self.assertEqual(mano_ramon, juego.cartas_por_jugador()["Román"])
        self.assertEqual("Román", juego.turno_de())


    def test_juego_inicia_con_tablero_en_cero(self) -> None:
        juego = self.juego_default_2p()

        tablero_de_color = juego.tablero()

        self.assertTrue(all(tablero_de_color[color] == 0 for color in self.colores()))

        
    def test_juego_bajar_carta_en_escalera(self) -> None:
        juego = self.juego_default_2p()
        juego.bajar(0)

        tablero_de_color = juego.tablero()

        self.assertEqual(1, tablero_de_color["Verde"])

    def test_juego_bajar_carta_completando_color_suma_pista(self) -> None:
        juego = self.juego_default_2p()

        # bajar del 1 al 4
        for _ in range(8):
            juego.bajar(0)
        
        # doy pista y bajo el 5
        juego.dar_pista("Color", "Amarillo", "Ramón")
        juego.bajar(0)

        self.assertEqual(7, juego.pistas_restantes())

    def test_juego_pifie_con_carta_bajada(self) -> None:
        juego = self.juego_default_2p()
        juego.bajar(1)

        tablero_de_color = juego.tablero()

        self.assertEqual(0, tablero_de_color["Verde"])
        self.assertEqual(2, juego.vidas())

    def test_juego_termina_si_se_queda_sin_vidas(self) -> None:
        juego = self.juego_default_2p()
        juego.bajar(1)
        juego.bajar(1)
        juego.bajar(1)

        self.assertEqual(0, juego.vidas())
        self.assertTrue(juego.terminado())

    def test_juego_tomar_accion_de_descarte(self) -> None:
        juego = self.juego_default_2p()
        
        accion = {
                'jugador': "Román",
                'accion': 'DESCARTAR',
                'carta': 0
        }
        juego.tomar_accion(accion)
        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(5, len(cartas_de["Román"]))
        self.assertFalse((1, "Verde") in cartas_de["Román"])
        self.assertTrue((5, "Azul") in cartas_de["Román"])
    
    def test_juego_tomar_accion_de_bajada(self) -> None:
        juego = self.juego_default_2p()
        
        accion = {
                'jugador': "Román",
                'accion': 'BAJAR',
                'carta': 0
        }

        juego.tomar_accion(accion)
        cartas_de = juego.cartas_por_jugador()

        self.assertEqual(5, len(cartas_de["Román"]))
        self.assertFalse((1, "Verde") in cartas_de["Román"])
        self.assertTrue((5, "Azul") in cartas_de["Román"])

    def test_juego_tomar_accion_de_dar_pista(self) -> None:
        jugadores = ["Román", "Ramón"]
        juego = Juego(jugadores, 3, Repartidor(self.mezclar_mazo_minimal_mezcladito))

        accion = {
                'jugador': "Román",
                'accion': 'PISTA',
                'pista_a': "Ramón",
                'tipo': "Color",
                'valor': "Amarillo"
        }

        juego.tomar_accion(accion)

        pistas_de = juego.pistas_por_jugador()
        self.assertTrue(all("Amarillo" in pistas_de["Ramón"][i] for i in [0, 2, 4]))
        self.assertTrue(all(len(pistas_de["Ramón"][i]) == 0 for i in [1, 3]))

    def test_juego_tomar_accion_tiene_que_ser_valida(self) -> None:
        juego = self.juego_default_2p()

        accion = {
                'jugador': "Román",
                'accion': 'INSTAWIN',
                'pista_a': "Ramón",
                'tipo': "Color",
                'valor': "Amarillo"
        }

        self.assertRaises(JuegoAccionInvalidaException,
                juego.tomar_accion, accion)

    def test_juego_tomar_accion_tiene_que_ser_del_que_le_corresponda_el_turno(self) -> None:
        juego = self.juego_default_2p()

        accion = {
                'jugador': "Ramón",
                'accion': 'PISTA',
                'pista_a': "Ramón",
                'tipo': "Color",
                'valor': "Amarillo"
        }

        self.assertRaises(JuegoTurnoDeOtroJugadorException,
                juego.tomar_accion, accion)
         
        
    
    def test_juego_terminado_no_puede_descartar(self) -> None:
        juego = self.juego_default_2p()
        juego.bajar(1)
        juego.bajar(1)
        juego.bajar(1)
        
        self.assertRaises(JuegoAccionEnPartidaTerminadaException,
                juego.descartar, 0)

    def test_juego_terminado_no_puede_bajar(self) -> None:
        juego = self.juego_default_2p() 
        juego.bajar(1)
        juego.bajar(1)
        juego.bajar(1)
        
        self.assertRaises(JuegoAccionEnPartidaTerminadaException,
                juego.bajar, 0)

    def test_juego_terminado_no_puede_dar_pistas(self) -> None:
        juego = self.juego_default_2p()
        juego.bajar(1)
        juego.bajar(1)
        juego.bajar(1)
        
        self.assertRaises(JuegoAccionEnPartidaTerminadaException,
                juego.dar_pista, "Número", 1, "Román")

    def test_estado_del_juego(self) -> None:
        juego = self.juego_default_2p()
        
        self.assertEqual(
                { 'global': {
                        'terminado': False,
                        'jugadores': ["Román", "Ramón"],
                        'turno_de': "Román",
                        'vidas': 3,
                        'pistas_restantes': 7,
                        'cartas_restantes': 10,
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
                    'estado_jugadores': {
                        'Román': {
                            'cartas': [(i, "Verde") for i in range(1, 6)],
                            'pistas': [[], [], [], [], []]
                        },
                        'Ramón': {
                            'cartas': [(i, "Rojo") for i in range(1,6)],
                            'pistas': [[], [], [], [], []]
                        }
                    }
                }, juego.estado())

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

    def juego_default_2p(self) -> 'Juego':
        jugadores = ["Román", "Ramón"]
        repartidor = self.repartidor_rojo_verde()
        juego = Juego(jugadores, 3, repartidor)
        return juego
        
    def juego_default_4p(self) -> 'Juego':
        jugadores = ["Román", "Ramón", "Morán", "norMa"]
        repartidor = self.repartidor_rojo_verde()
        juego = Juego(jugadores, 3, repartidor)
        return juego

    def colores(self) -> List[str]:
        return [
            "Rojo",
            "Azul",
            "Verde",
            "Amarillo",
            "Blanco",
        ]

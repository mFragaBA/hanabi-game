# pyre-strict
from typing import List, Dict, Tuple, Union, Set, Any
from model.exceptions import *
from model.repartidor import Repartidor
from model.pista import Pista

class Juego():

    def __init__(self,
            jugadores: List[str] = [],
            vidas_iniciales: int = 3,
            repartidor: 'Repartidor' = Repartidor.repartidor_estandar(),
            ) -> None:
        self.validar_jugadores(jugadores)
        self._terminado = False
        self._jugadores = jugadores
        self._turno_de = 0
        self._puntaje = 0
        self._pistas_restantes = 7
        self._vidas = vidas_iniciales
        self._repartidor = repartidor
        tamanio_mano = 5 if len(jugadores) < 4 else 4

        self._cartas_por_jugador = {}
        self._pistas_por_jugador = {}
        for jugador in self._jugadores:
            self._cartas_por_jugador[jugador] = self._repartidor.repartir(tamanio_mano)
            self._pistas_por_jugador[jugador] = [set() for _ in range(tamanio_mano)]

        self._tablero = {
            "Rojo": 0,
            "Verde": 0,
            "Azul": 0,
            "Blanco": 0,
            "Amarillo": 0,
        }


    def validar_jugadores(self, jugadores: List[str]) -> None:
        if len(jugadores) < 2:
            raise JuegoSinJugadoresSuficientesException()
        if len(jugadores) > 5:
            raise JuegoConDemasiadosJugadoresException()
        if any(jugadores.count(jugador) > 1 for jugador in jugadores):
            raise JuegoConJugadoresDuplicadosException()

    def descartar(self, carta : int) -> None:
        self._validar_partida_en_curso()

        jugador = self.turno_de()
        self._validar_pos_carta_para(jugador, carta)

        self._tirar_carta(jugador, carta)
        
        self._agregar_pista()
        self._cambiar_turno()

    def bajar(self, carta : int) -> None:
        self._validar_partida_en_curso()
        jugador = self.turno_de()

        self._validar_pos_carta_para(jugador, carta)

        numero = self._cartas_por_jugador[jugador][carta][0]
        color = self._cartas_por_jugador[jugador][carta][1]

        if numero == self._tablero[color] + 1:
            self._tablero[color] = numero

            if numero == 5:
                self._agregar_pista()
        else:
            self._quitar_vida()

        self._tirar_carta(jugador, carta)
        self._cambiar_turno()

    def estado(self) -> Dict[str, Any]:
        pistas_de_adaptado = {}
        for jugador in self._jugadores:
            pistas_de_jugador = self._pistas_por_jugador[jugador]
            pistas_de_adaptado[jugador] = [list(pistas) for pistas in pistas_de_jugador]
        
        return {
            'terminado': self._terminado,
            'jugadores': self._jugadores,
            'turno_de': self.turno_de(),
            'vidas': self._vidas,
            'pistas_restantes': self._pistas_restantes,
            'cartas_restantes': self._repartidor.cartas_restantes(),
            'cartas_de': self._cartas_por_jugador,
            'pistas_de': pistas_de_adaptado,
            'tablero': self._tablero,
            'puntaje': 0,
            'descarte': {
                'Rojo': [],
                'Azul': [],
                'Amarillo': [],
                'Verde': [],
                'Blanco': []
            }
        }

    def _validar_pos_carta_para(self, jugador: str, carta: int) -> None:
        if len(self._cartas_por_jugador[jugador]) <= carta:
            raise JuegoDescartaCartaFueraDeManoException()

    def _tirar_carta(self, jugador: str, carta: int) -> None:
        self._cartas_por_jugador[jugador].pop(carta)
        self._pistas_por_jugador[jugador].pop(carta)

        if not self._repartidor.mazo_vacio():
            self._cartas_por_jugador[jugador].append(self._repartidor.repartir(1)[0])
            self._pistas_por_jugador[jugador].append(set())

    def dar_pista(self, tipo: str, valor: Union[int, str], jugador: str) -> None:
        self._validar_partida_en_curso()
        if jugador not in self._jugadores:
            raise JuegoPistaSinDestinatarioException()

        if self._pistas_restantes == 0:
            raise JuegoSinPistasDisponiblesException()

        if jugador == self.turno_de():
            raise JuegoPistaASiMismoException()

        cartas_del_jugador = self._cartas_por_jugador[jugador]
        pistas_del_jugador = self._pistas_por_jugador[jugador]
        pista = Pista.pista_para(tipo, valor).aplicar_a(cartas_del_jugador, pistas_del_jugador)
        self._cambiar_turno()
        self._quitar_pista()

    def _cambiar_turno(self) -> None:
        self._turno_de = (self._turno_de + 1) % len(self._jugadores)

    def _validar_partida_en_curso(self) -> None:
        if self._terminado:
            raise JuegoAccionEnPartidaTerminadaException()

    def jugadores(self) -> List[str]:
        return self._jugadores

    def puntaje(self) -> int:
        return self._puntaje
    
    def vidas(self) -> int:
        return self._vidas

    def _quitar_vida(self) -> None:
        self._vidas -= 1

        if self._vidas == 0:
            self._terminado = True

    def tablero(self) -> Dict[str, int]:
        return self._tablero

    def pistas_restantes(self) -> int:
        return self._pistas_restantes

    def _agregar_pista(self) -> None:
        self._pistas_restantes = min(self._pistas_restantes + 1, 7)

    def _quitar_pista(self) -> None:
        self._pistas_restantes -= 1

    def turno_de(self) -> str:
        return self._jugadores[self._turno_de]

    def cartas_por_jugador(self) -> Dict[str, List[Tuple[int, str]]]:
        return self._cartas_por_jugador

    def pistas_por_jugador(self) -> Dict[str, List[Set[str]]]:
        return self._pistas_por_jugador

    def terminado(self) -> bool:
        return self._terminado


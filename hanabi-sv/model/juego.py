# pyre-strict
from typing import List, Dict, Tuple, Union, Set
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


    def validar_jugadores(self, jugadores: List[str]) -> None:
        if len(jugadores) < 2:
            raise JuegoSinJugadoresSuficientesException()
        if len(jugadores) > 5:
            raise JuegoConDemasiadosJugadoresException()
        if any(jugadores.count(jugador) > 1 for jugador in jugadores):
            raise JuegoConJugadoresDuplicadosException()

    def descartar(self, carta : int) -> None:
        jugador = self.turno_de()

        if len(self._cartas_por_jugador[jugador]) <= carta:
            raise JuegoDescartaCartaFueraDeManoException()

        self._cartas_por_jugador[jugador].pop(carta)
        self._pistas_por_jugador[jugador].pop(carta)
        

        if not self._repartidor.mazo_vacio():
            self._cartas_por_jugador[jugador].append(self._repartidor.repartir(1))
            self._pistas_por_jugador[jugador].append(set())
        
        self._cambiar_turno()

    def dar_pista(self, tipo: str, valor: Union[int, str], jugador: str) -> None:
        if jugador not in self._jugadores:
            raise JuegoPistaSinDestinatarioException()

        cartas_del_jugador = self._cartas_por_jugador[jugador]
        pistas_del_jugador = self._pistas_por_jugador[jugador]
        pista = Pista.pista_para(tipo, valor, self).aplicar_a(cartas_del_jugador, pistas_del_jugador)

    def _cambiar_turno(self) -> None:
        self._turno_de = (self._turno_de + 1) % len(self._jugadores)

    def jugadores(self) -> List[str]:
        return self._jugadores

    def puntaje(self) -> int:
        return self._puntaje
    
    def vidas(self) -> int:
        return self._vidas

    def pistas_restantes(self) -> int:
        return self._pistas_restantes

    def turno_de(self) -> str:
        return self._jugadores[self._turno_de]

    def cartas_por_jugador(self) -> Dict[str, List[Tuple[int, str]]]:
        return self._cartas_por_jugador

    def pistas_por_jugador(self) -> Dict[str, List[Set[str]]]:
        return self._pistas_por_jugador


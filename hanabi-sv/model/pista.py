# pyre-strict

from typing import Union, Dict, Set, List
from model.exceptions import *


class Pista():

    def __init__(self, tipo: str, valor: Union[str, int], juego: 'Juego') -> None:
        self._tipo = tipo
        self._valor = valor
        self._juego = juego

    def aplicar_a(self, cartas, pistas):
        raise NotImplementedError


    @classmethod
    def pista_para(cls, tipo: str, valor: Union[str, int], juego: 'Juego') -> 'Pista':
        for sub_cls in cls.__subclasses__():
            if sub_cls.para(tipo):
                return sub_cls(tipo, valor, juego)

        raise JuegoTipoDePistaInvalidoException

class PistaColor(Pista):

    def __init__(self, tipo: str, valor: str, juego: 'Juego') -> None:
        super().__init__(tipo, valor, juego)

    def aplicar_a(self, cartas, pistas):
        for i in range(len(cartas)):
            if cartas[i][1] == self._valor:
                pistas[i].add(self._valor)
        self._juego._cambiar_turno()

    @classmethod
    def para(cls, tipo: str) -> bool:
        return tipo == "Color"

class PistaNumero(Pista):

    def __init__(self, tipo: str, valor: str, juego: 'Juego') -> None:
        super().__init__(tipo, valor, juego)

    def aplicar_a(self, cartas, pistas):
        for i in range(len(cartas)):
            if cartas[i][0] == self._valor:
                pistas[i].add(str(self._valor))
        self._juego._cambiar_turno()

    @classmethod
    def para(cls, tipo: str) -> bool:
        return tipo == "Número"

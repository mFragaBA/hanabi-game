

class JuegoSinJugadoresSuficientesException(Exception):
    def __init__(self, msg: str = 'Tienen que haber al menos 2 jugadores en la partida') -> None:
        super().__init__(msg)

class JuegoConDemasiadosJugadoresException(Exception):
    def __init__(self, msg: str = 'Pueden haber a lo sumo 4 jugadores por partida') -> None:
        super().__init__(msg)

class JuegoConJugadoresDuplicadosException(Exception):
    def __init__(self, msg: str = 'El nombre de cada jugador tiene que ser único') -> None:
        super().__init__(msg)

class JuegoDescartaCartaFueraDeManoException(Exception):
    def __init__(self, msg: str = 'La Carta a descartar tiene que estar en la mano del jugador') -> None:
        super().__init__(msg)

class JuegoTipoDePistaInvalidoException(Exception):
    def __init__(self, msg: str = 'Las pistas son por color o por número') -> None:
        super().__init__(msg)

class JuegoPistaSinDestinatarioException(Exception):
    def __init__(self, msg: str = 'Las pistas tiene que ser a un jugador de la mesa') -> None:
        super().__init__(msg)

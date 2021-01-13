

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

class JuegoSinPistasDisponiblesException(Exception):
    def __init__(self, msg: str = 'Tiene que haber al menos una pista para darla') -> None:
        super().__init__(msg)

class JuegoPistaASiMismoException(Exception):
    def __init__(self, msg: str = 'No puede darse una pista a sui mismo') -> None:
        super().__init__(msg)

class JuegoAccionEnPartidaTerminadaException(Exception):
    def __init__(self, msg: str = 'La partida ya finalizo') -> None:
        super().__init__(msg)

class JuegoAccionInvalidaException(Exception):
    def __init__(self, msg: str = 'Acción inválida. Tiene que ser una entre DESCARTAR, BAJAR, PISTA') -> None:
        super().__init__(msg)

class JuegoTurnoDeOtroJugadorException(Exception):
    def __init__(self, msg: str = 'Acción inválida. No es el turno de quien realiza la acción') -> None:
        super().__init__(msg)

class JugadorExistenteException(Exception):
    def __init__(self, msg: str = 'Un jugador con el mismo nombre ya está en la sala') -> None:
        super().__init__(msg)

class JugadorInExistenteException(Exception):
    def __init__(self, msg: str = 'No hay ningún jugador con dicho nombre en una sala') -> None:
        super().__init__(msg)

class LobbyCompletoException(Exception):
    def __init__(self, msg: str = 'La sala está completa') -> None:
        super().__init__(msg)

class JugadorInexistenteException(Exception):
    def __init__(self, msg: str = 'No se encontró a dicho jugador') -> None:
        super().__init__(msg)

class LobbyExistenteException(Exception):
    def __init__(self, msg: str = 'Ya existe un lobby con ese nombre') -> None:
        super().__init__(msg)

class LobbyInexistenteException(Exception):
    def __init__(self, msg: str = 'No existe un lobby con ese nombre') -> None:
        super().__init__(msg)

class NombreInvalidoException(Exception):
    def __init__(self, msg: str = 'Ese nombre no es válido') -> None:
        super().__init__(msg)

class PartidaYaIniciadaException(Exception):
    def __init__(self, msg: str = 'No se puede unir a una partida ya iniciada') -> None:
        super().__init__(msg)

class PartidaNoIniciadaException(Exception):
    def __init__(self, msg: str = 'La partida no inició todavía') -> None:
        super().__init__(msg)

class JugadorEnPartidaExceptioPartidaNoIniciadaExceptionn(Exception):
    def __init__(self, msg: str = 'No se puede sacar al jugador si todavía está en una partida') -> None:
        super().__init__(msg)

class JugadorInExistenteEnLobbyException(Exception):
    def __init__(self, msg: str = 'No se puede sacar al jugador porque no está en esa sala') -> None:
        super().__init__(msg)


import React from 'react'
import Mano from './Mano.js'
import Carta from './Carta.js'

class JuegoView extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			jugador: props.jugador,
		};
	}

	componentDidMount() {
		this.props.socket.on('juego_update', this.handleJuegoUpdate);
		this.props.socket.on('estado_expirado', this.actualizarEstadoDelJuego);
		this.actualizarEstadoDelJuego();
	}

	componentWillUnmount() {
		this.props.socket.off('juego_update', this.handleJuegoUpdate);
		this.props.socket.off('estado_expirado', this.actualizarEstadoDelJuego);
	}

	actualizarEstadoDelJuego = () => {
		this.props.socket.emit('estado_juego_update');
	}

	handleJuegoUpdate = (data) => {
		console.log('llegó update', data);

		this.setState({
			accion: '',
			global: data.global,
			estado_jugadores: data.estado_jugadores,
		},
		() => {
			console.log("estado:", this.state);
		});
	}

	registrarYResetear = (accion) => {
		this.props.socket.emit('registrar_accion', accion);
		this.setState({
			accion: '',
		},
		() => {
			console.log("estado actualizado:",this.state);
		});
	}

	elegirPista = (pistaStr) => {
		this.setState({
			accion: 'pista',
			seleccion: pistaStr,
		});
	}

	elegirCarta = (jugador, carta_info) => {
		let index = carta_info.index;
		console.log("index: ", index);
		if (this.state.accion === 'cartaElegida' && index === this.state.seleccion) {
			console.log("Carta Elegida - estado reseteado");
			this.setState({
				accion: '',
			});
		} else {
			console.log("Carta Elegida - estado seteado");
			this.setState({
				accion: 'cartaElegida',
				seleccion: index,
			});
		}
	}

	darPista = (jugador, carta_info) => {
		if (this.state.accion === 'pista'){
			let accion = {
				jugador: this.state.jugador,
				accion: 'PISTA',
				pista_a: jugador,
				tipo: this.state.seleccion,
				valor: carta_info[this.state.seleccion],
			};
			this.registrarYResetear(accion);
		}
	}

	bajarCarta = () => {
		if (this.state.accion === 'cartaElegida') {
			let accion = {
				jugador: this.props.jugador,
				accion: 'BAJAR',
				carta: this.state.seleccion,
			};
			this.registrarYResetear(accion);
		}
	}

	descartarCarta = () => {
		if (this.state.accion === 'cartaElegida') {
			let accion = {
				jugador: this.props.jugador,
				accion: 'DESCARTAR',
				carta: this.state.seleccion,
			};
			this.registrarYResetear(accion);
		}
	}

	dummy = (dum, dumdum) => {
		console.log("dummy");
	}

	tablero = () => {
		let cartas_en_juego = []

		for (const [ clave, value ] of Object.entries(this.state.global.tablero)) {
			cartas_en_juego.push([value, clave]);
		}

		return cartas_en_juego;
	}

	descarte() {
		let backColor = {
			Amarillo: "bg-yellow-400",
			Azul: "bg-blue-400",
			Verde: "bg-green-400",
			Blanco: "bg-white",
			Rojo: "bg-red-400",
		}
		return ( 
			<div className="flex flex-col p-5">
			{ Object.entries(this.state.global.descarte).map( ([color, numeros]) => 
				<div className="flex flex-row">
					{numeros.map( (numero, index) =>
						<div className={"m-0.5 flex-none border rounded text-black " + backColor[color]}>
							{numero}
						</div>
					)}
				</div>
			)}
			</div>
		);
	}

	render() {

		if (this.state && this.state.global && this.state.estado_jugadores) {

			return (
				<div className="flex flex-row items-start">
					<div className="text-2xl">
						<div className="border border-green-400 rounded bg-dorso bg-contain w-28 h-36 flex justify-center items-center">
							{this.state.global.cartas_restantes}	
						</div>
					</div>
					<div className="flex flex-col flex-grow bg-green-700 border border-yellow-500 rounded mx-2">
						<div className="flex flex-row justify-center my-1">
							<button type="button" className="rounded border border-black bg-white text-2xl" onClick={this.descartarCarta}>Descartar</button>
						</div>
						<div className="flex flex-row justify-center text-2xl my-1">
							<button type="button" className={"rounded mr-3 border border-black " + ((this.state.accion === 'pista' && this.state.seleccion === 'Color') ? "bg-red-400" : "bg-white")} onClick={ () => this.elegirPista("Color")}>
								Pista-Color	
							</button>

							<button type="button" className={"rounded ml-3 border border-black " + ((this.state.accion === 'pista' && this.state.seleccion === 'Numero') ? "bg-red-400" : "bg-white")} onClick={ () => this.elegirPista("Numero")}>
								Pista-Numero	
							</button>
						</div>
						
						<div className="flex flex-row justify-center" onClick={this.bajarCarta}>	
							{this.tablero().map((carta, index) => 
								<div className="m-1">
									<Carta key={index} numero={carta[0]} color={carta[1]} onCartaSeleccion={this.dummy} pistas={[]}/>
								</div>
							)}	

						</div>
						<div className="flex flex-col items-center">
							<div>
							Vidas: {this.state.global.vidas}
							</div>
							<div>
							Pistas Restantes: {this.state.global.pistas_restantes}
							</div>
						</div>
						{this.descarte()}
					</div>
					<div className="flex flex-col">
						{Object.keys(this.state.estado_jugadores).map((key, index) => this.props.jugador !== key ?
						<Mano key={index} jugador={key} mano={this.state.estado_jugadores[key]} onCartaSeleccion={this.darPista} cartaElegida={ -1 } turnoDelJugador={key === this.state.global.turno_de} /> : <Mano key={index} jugador={key} mano={this.state.estado_jugadores[key]} onCartaSeleccion={this.elegirCarta} cartaElegida={ this.state.accion === 'cartaElegida' ? this.state.seleccion : -1} turnoDelJugador={key === this.state.global.turno_de} />
						)}
					</div>
				</div>
			);

		}

		return (
			<div></div>
		);
	}
}

export default JuegoView;

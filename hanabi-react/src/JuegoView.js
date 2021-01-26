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

	render() {

		if (this.state && this.state.global && this.state.estado_jugadores) {

			return (
				<div className="flex flex-row">
					<div className="text-2xl">
						<div className="border border-green-400 rounded bg-dorso bg-contain w-28 h-36 flex justify-center items-center">
							{this.state.global.cartas_restantes}	
						</div>
					</div>
					<div className="flex flex-col flex-grow bg-green-700 border border-yellow-500 rounded mx-2">
						<div className="flex flex-row justify-center">
							<button type="button" className="rounded border border-black bg-white text-2xl" onClick={this.descartarCarta}>Descartar</button>
						</div>
						<div className="flex flex-row justify-center text-2xl">
							<button type="button" className="rounded mr-3 border border-black bg-white" onClick={ () => this.elegirPista("Color")}>
								Pista-Color	
							</button>

							<button type="button" className="rounded ml-3 border border-black bg-white" onClick={ () => this.elegirPista("Numero")}>
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
					</div>
					<div className="flex flex-col">
						{Object.keys(this.state.estado_jugadores).map((key, index) => this.props.jugador !== key ?
						<Mano key={index} jugador={key} mano={this.state.estado_jugadores[key]} onCartaSeleccion={this.darPista} /> : <Mano key={index} jugador={key} mano={this.state.estado_jugadores[key]} onCartaSeleccion={this.elegirCarta} />
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

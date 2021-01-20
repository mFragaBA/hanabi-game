import React from 'react'
import Mano from './Mano.js'

class JuegoView extends React.Component {

	constructor(props) {
		super(props);
		this.setState({
			jugador: props.jugador,
			jugadores: props.jugadores,
			terminado: false,
		});
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
		delete data['global']['jugadores'];

		this.setState(data);
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
				<div className="flex flex-col flex-grow border border-yellow-500">
				
				</div>
				<div className="flex flex-col">
					{Object.keys(this.state.estado_jugadores).map((key, index) => 
					<Mano jugador={key} mano={this.state.estado_jugadores[key]} onCardSelection={()=>{}} />
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

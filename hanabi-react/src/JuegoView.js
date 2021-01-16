import React from 'react'

class JuegoView extends React.Component {

	constructor(props) {
		super(props);
	}

	componentWillMount() {
		this.props.socket.on('juego_update', this.handleJuegoUpdate);
		this.props.socket.on('estado_expirado', this.actualizarEstadoDelJuego);
		this.actualizarEstadoDelJuego();
	}

	actualizarEstadoDelJuego = () => {
		this.props.socket.emit('estado_juego_update');
	}

	handleJuegoUpdate = () => {
		console.log('llegó update');
	}

	render() {
		return (<div></div>);
	}
}

export default JuegoView;

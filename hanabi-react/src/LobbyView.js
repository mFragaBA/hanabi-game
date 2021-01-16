import React from 'react'
import ListaSeleccionable from './ListaSeleccionable.js'

class LobbyView extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			view: 'ListarLobbiesView',
			jugador: props.jugador,
			lobby: props.lobby,
			jugadores: [],
		};
	}

	componentDidMount() {
		this.props.socket.on('lobby_update', this.handleLobbyUpdate);
		this.props.socket.emit('estado_lobby_update');
	}

	componentWillUnmount() {
		this.props.socket.off('lobby_update', this.handleLobbyUpdate)
	}

	handleLobbyUpdate = (estado) => {
		console.log(estado)
		this.setState({
			jugadores: estado['jugadores'],
		});
	}

	handleIniciarPartida() {
		this.props.socket.emit('iniciar_partida')	
	}

	render() {
		return (
			<div className="flex flex-col h-full">
				<div className="flex-grow flex flex-col p-5 text-2xl bg-opacity-30 bg-green-300 border border-yellow-500 rounded">
					<div className="text-center"> Jugadores en el Lobby </div>
					<div className="flex flex-row flex-grow">
						<div className="flex-grow">
							<ListaSeleccionable items={this.state.jugadores} accion={this.handleLobbySeleccionado}/>
						</div>
					</div>
				</div>
				<div className="flex-none text-center">
					<button type="button" className="flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2" onClick={() => { this.handleIniciarPartida() }}>
						Iniciar Partida
					</button>
				</div>
			</div>
		);
	}
}

export default LobbyView;

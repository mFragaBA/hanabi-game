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
    		this.props.socket.on('estado_expirado', this.handleEstadoExpirado);
		this.props.socket.emit('estado_lobby_update');
	}

	componentWillUnmount() {
		this.props.socket.off('lobby_update', this.handleLobbyUpdate)
    		this.props.socket.off('estado_expirado', this.handleEstadoExpirado);
	}

	handleLobbyUpdate = (estado) => {
		this.setState({
			jugadores: estado['jugadores'],
		});
	}

	handleEstadoExpirado = () => {
		this.props.socket.emit('estado_lobby_update'); 
	}

	handleIniciarPartida() {
		this.props.socket.emit('iniciar_partida')	
	}

	handleJugadorSeleccionado = (jugador, index) => {
		console.log(jugador);
	}

	render() {
		const css = `
			  #scroll-plist::-webkit-scrollbar {
				    width: 4px;
				    cursor: pointer;
				    /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/

				}
				#scroll-plist::-webkit-scrollbar-track {
				    background-color: rgba(229, 231, 235, var(--bg-opacity));
				    cursor: pointer;
				    /*background: red;*/
				}
				#scroll-plist::-webkit-scrollbar-thumb {
				    cursor: pointer;
				    background-color: #a0aec0;
				    /*outline: 1px solid slategrey;*/
				}
			`

		return (
			<div className="flex flex-col h-4/5">
				<style>{css}</style>
				<div className="flex-grow flex flex-row p-5 text-2xl bg-opacity-100 bg-gray-900 border border-yellow-500 rounded max-h-full justify-between">
					<div id="scroll-plist" className="w-1/3 flex flex-col overflow-y-scroll mr-5">
						{this.state.jugadores.map((item, index) =>
								<div key={index} className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1" onClick={ () => this.handleJugadorSeleccionado(item, index)}>
									{item}
								</div>
						)}
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
						<div className="text-center bg-gray-600 rounded text-white border border-gray-400 shadow-xl m-1">asd</div>
					</div>
					<div className="flex-grow flex flex-col bg-gray-600 text-white rounded border border-gray-400 mb-2 p-5 max-w-full">
						<div className="text-center">
							Partida de Hanabi
						</div>

						<ul>
							<li>Vidas Iniciales: 3</li>
							<li>Pistas Iniciales: 7</li>
							<li>Modo de Juego: Clásico</li>
						</ul>
					</div>
				</div>
				<div className="flex-none text-center">
					<button type="button" className="flex-initial focus:ring bg-opacity-100 border-opacity-30 bg-gray-900 hover:bg-yellow-500 text-white font-semibold py-2 px-4 border border-yellow-500 rounded m-2" onClick={() => { this.handleIniciarPartida() }}>
						Iniciar Partida
					</button>
				</div>
			</div>
		);
	}
}

export default LobbyView;

import React from 'react'
import './css/Common.css'
//import './css/Intro.css'

class HomeView extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			jugador: '',
			lobby: '',
		};
	}

	handleCambioDeNombre(event) {
		let jugador = event.target.value;
		this.setState({jugador: jugador});
		this.props.app.setState({jugador: jugador});
	}

	handleCambioDeLobby(event) {
		let lobby = event.target.value;
		this.setState({lobby: lobby});
	}

	handleCrearLobbySubmit(event) {
		event.preventDefault();
		let jugador = this.state.jugador;
		let lobby = this.state.lobby;

		if (jugador && lobby) {
			this.props.socket.emit('crear_lobby', {
				'player_name': jugador,
				'lobby_name': lobby
			});
		}


	}

	handleMostrarLobbies(event) {
		event.preventDefault();
		let jugador = this.state.jugador;
		let lobby = this.state.lobby;

		this.props.app.setState({
			view: 'ListaLobbiesView',
			jugador: jugador,
			lobby: lobby
		})

	}

	campoInput(titulo, texto, callback) {
		return (
			<div className="flex flex-row justify-center">
				<div className="py-4 ml-4 flex-none w-16 h-16"> {titulo} </div>
				<div className="py-2 flex-grow h-16">
					<input className="border py-2 px-3 text-grey-darkest mx-2 rounded" type="text" value={texto} onChange={callback} /> 
				</div>
		</div>
		)
	}

	render() {
		return (
			<div className="flex flex-col h-full">
				<div className="h-4/5"></div>
				<div className="flex flex-col font-cursive">
					<div className="">
						<form onSubmit={event => this.handleCrearLobbySubmit(event)}>
							<div className="flex flex-row">
								<div className="flex-auto bg-opacity-30 border-opacity-30 bg-blue-300 mx-5 font-semibold rounded text-black-400 border border-yellow-500">
								{this.campoInput("Nombre", this.state.jugador, (event) => { this.handleCambioDeNombre(event) } ) }
								{this.campoInput("Lobby", this.state.lobby, (event) => { this.handleCambioDeLobby(event) })}
								</div>
								<div className="flex-auto flex flex-col">
									<input className="flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-green-300 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2" type="submit" value="Crear Lobby" />
									<button type="button" className="flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2" onClick={(event) => { this.handleMostrarLobbies(event) }}>
										Ver salas disponibles 	
									</button>
								</div>
							</div>
						</form>
					</div>
				</div>
			</div>
		);
	}
}

export default HomeView;

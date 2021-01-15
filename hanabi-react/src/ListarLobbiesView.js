import React from 'react'
import ListaSeleccionable from './ListaSeleccionable.js'

class ListarLobbiesView extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			view: 'ListarLobbiesView',
			lobby: '',
		};
	}

	componentDidMount() {
		this.props.socket.on('lista_lobbies', this.handleListaLobbyUpdate);
		this.props.socket.emit('listar_lobbies');
	}

	componentWillUnmount() {
		this.props.socket.off('lista_lobbies', this.handleListaLobbyUpdate);
	}

	handleListaLobbyUpdate = data => {
		console.log("LLegaron los lobbies!");
		this.setState({
			lobbies: data,
		});
	}

	handleLobbySeleccionado = (lobby, index) => {
		console.log(lobby + " - " + index);
		this.selectedLobby = lobby;
	}

	handleEntrarALobby() {
		if (this.selectedLobby) {
			let pname = this.props.app.state.jugador
			console.log("p: " + pname);
			this.props.socket.emit('unirse_a_lobby',
				{
					player_name: pname,
					lobby_name: this.selectedLobby,
				})	
		}
	}

	render() {
		return (
			<div className="flex flex-row">
				<div className="flex-grow">
				<ListaSeleccionable items={this.state.lobbies} accion={this.handleLobbySeleccionado}/>
				</div>
				<div className="flex-none">
					<button type="button" className="flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2" onClick={() => { this.handleEntrarALobby() }}>
						Entrar Al Lobby
					</button>
				</div>
			</div>
		);
	}
}

export default ListarLobbiesView;

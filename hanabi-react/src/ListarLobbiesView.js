import React from 'react'
import ListaLobbies from './ListaLobbies.js'

class ListarLobbiesView extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			view: 'ListarLobbiesView',
			lobby: '',
		};
	}

	componentDidMount() {
		this.actualizar();
	}

	actualizar = () => {
		fetch(this.props.url + '/listar_lobbies')
			.catch(
				(error) => {
					console.log(error);
				}
			)
			.then( response => {
				console.log('response: ', response);
				return response.json();
			})
			.then( data => this.handleListaLobbyUpdate(data['lobbies']));
	}

	handleListaLobbyUpdate = data => {
		this.setState({
			lobbies: data,
		});
	}

	handleLobbySeleccionado = (lobby, index) => {
		this.selectedLobby = lobby.nombre;
	}

	handleEntrarALobby() {
		if (this.selectedLobby) {
			let pname = this.props.app.state.jugador
			this.props.actualizarLobby(this.selectedLobby);

			fetch(this.props.url + '/unirse_a_lobby?player=' + pname + '&lobby=' + this.selectedLobby + '&c_id=' + this.props.cId)
				.catch(
					(error) => {
						console.log(error);
					}
				)
				.then( this.props.handleSentarseEnMesa(this.selectedLobby) );
		}
	}

	render() {
		return (
			<div className="flex flex-row h-full pt-20">
				<div className="flex-grow mx-20 mb-20 p-10 bg-opacity-30 bg-green-300 border border-yellow-500 rounded">
					<ListaLobbies lobbies={this.state.lobbies} accion={this.handleLobbySeleccionado}/>
				</div>
				<div className="flex-none flex flex-col mr-10">
					<button type="button" className="flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2" onClick={() => { this.handleEntrarALobby() }}>
						Entrar Al Lobby
					</button>
					<button type="button" className="flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2" onClick={() => { this.actualizar() }}>
						Actualizar
					</button>
				</div>
			</div>
		);
	}
}

export default ListarLobbiesView;

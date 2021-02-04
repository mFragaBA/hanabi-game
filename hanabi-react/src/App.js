import React from 'react'
import io from 'socket.io-client'
import './App.css';
import HomeView from './HomeView.js'
import ListarLobbiesView from './ListarLobbiesView.js'
import LobbyView from './LobbyView.js'
import JuegoView from './JuegoView.js'

const url = process.env.NODE_ENV === 'production'
	? "https://fierce-sea-39458.herokuapp.com" : "http://localhost:5000"

const socket = io(url)

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			view: 'HomeView',
			jugador: '',
			lobby: '',
		};
	}

	componentDidMount() {
		socket.on('partida_iniciada', () => {
			this.handlePartidaIniciada()
		});
		socket.on('partida_terminada', () => {
			this.handlePartidaTerminada()
		});
		socket.on('unido_a_lobby', (lobby) => {
			this.handleEntrarALobby(lobby)
		});
		socket.on('disconnect', (reason) => {
			console.log('Desconectado. Motivo:', reason);
			if (reason === 'io server disconnect') {
				// the disconnection was initiated by the server, you need to reconnect manually
				socket.connect();
			}
			// else the socket will automatically try to reconnect
		});
	}

	handleEntrarALobby(lobby){
		this.setState({
			view: 'LobbyView',
			lobby: lobby,
		});
	}

	handlePartidaIniciada() {
		this.setState({
			view: 'JuegoView',
		});
	}

	viewMatchingState() {	
		if (this.state.view === 'HomeView') {
			return ( <HomeView app={this} socket={socket}/> );
		}
		
		
		if (this.state.view === 'ListaLobbiesView') {
			return ( <ListarLobbiesView app={this} socket={socket}/>);
		}
		
		if (this.state.view === 'LobbyView') {
			return (<LobbyView
				app = {this}
				player = {this.state.jugador}
				lobby = {this.state.lobby}
				socket={socket}/>);
		}
		
		if (this.state.view === 'JuegoView') {
			return (<JuegoView
				app = {this}
				jugador = {this.state.jugador}
				socket = {socket}/>);
		}

		return (
			<div>
				La view es inválida ({this.state.view})
			</div>
		)
	}

	render() {
		return (
			<div className="min-h-screen bg-cover bg-scroll bg-no-repeat bg-hanabi">
				<div className="h-screen p-20 overflow-auto">
					{ this.viewMatchingState() }
				</div>
			</div>
		)
	}
}

export default App;

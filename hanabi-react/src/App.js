import React from 'react'
import './App.css';
import HomeView from './HomeView.js'
import ListarLobbiesView from './ListarLobbiesView.js'
import MesaView from './MesaView.js'

const url = process.env.NODE_ENV === 'production'
	? "https://fierce-sea-39458.herokuapp.com" : "http://localhost:5000"

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			loaded: false,
			error: null,
			view: 'HomeView',
			jugador: '',
			lobby: '',
		};
	}

	componentDidMount() {
		let cIdCookie = document.cookie
			.split('; ')
			.find(row => row.startsWith('c_id='))

		if (cIdCookie) {
		  	cIdCookie = cIdCookie.split('=')[1];
			this.setState({loaded: true});
		} else {

			fetch(url + '/session')
				.catch(
					(error) => {
						console.log(error);
					}
				)
				.then(response => response.json())
				.then(
					(result) => {
						document.cookie = "c_id=" + result['session']
						this.setState({
							loaded: true
						});
					},
					(error) => {
						this.setState({
							loaded: true,
							error: error,
						});
					}
				)
				.catch(error => console.log(error));
		}
	}

	handleSentarseEnMesa = (lobby) => {
		this.setState({
			view: 'MesaView',
			lobby: lobby,
		});
	}

	handleMostrarLobbies = () => {
		if (this.state.jugador) {
			this.setState({
				view: 'ListaLobbiesView',
			})
		}
	}

	actualizarJugador = (jugador) => {
		this.setState({jugador: jugador});
	}

	actualizarLobby = (lobby) => {
		this.setState({lobby: lobby});
	}

	viewMatchingState() {	
		const cIdValue = document.cookie.split('; ')
			.find(row => row.startsWith('c_id='))
			.split('=')[1];
		if (this.state.view === 'HomeView') {
			return ( <HomeView app={this}
				url={url}
				cId={cIdValue}
				handleMesaCreada={this.handleSentarseEnMesa} 
				handleMostrarLobbies={this.handleMostrarLobbies}
				actualizarJugador={this.actualizarJugador}
				actualizarLobby={this.actualizarLobby} /> );
		}
		
		
		if (this.state.view === 'ListaLobbiesView') {
			return ( <ListarLobbiesView app={this}
				url={url}
				cId={cIdValue}
				handleSentarseEnMesa={this.handleSentarseEnMesa}
				actualizarLobby={this.actualizarLobby} />);
		}

		if (this.state.view === 'MesaView') {
			console.log('estado jugador:', this.state.jugador);
			return ( <MesaView app={this} url={url} cId={cIdValue} jugador={this.state.jugador} lobby={this.state.lobby} />);
		}
		
		return (
			<div>
				La view es inválida ({this.state.view})
			</div>
		)
	}

	render() {
		const {loaded, error} = this.state;

		if (error) {
			return (
				<div className="flex flex-col">
					<div>
						Error generando la sessión. Intentá actualizando o limpiando las cookies.
					</div>
					<div>
						Error: {error}
					</div>
				</div>
			);
		} else if (!loaded) {
			return (
				<div className="min-h-screen bg-cover bg-scroll bg-no-repeat bg-hanabi">
					Generando la sesión...
				</div>
			);
		}

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

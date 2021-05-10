import React from 'react'
import './App.css';
import EntranceView from './EntranceView.js'
import HomeView from './HomeView.js'
import ListarLobbiesView from './ListarLobbiesView.js'
import MesaView from './MesaView.js'

const url = process.env.NODE_ENV === 'production'
	? "https://fierce-sea-39458.herokuapp.com" : "http://localhost:5000"

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			loaded_session: false,
			error: null,
			view: 'EntranceView',
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
			this.setState({view: 'HomeView'});
		}
	}

	handleEntrarAsGuest = () => {
		this.setState({
			view: 'HomeView',
		});
	}

	handleSentarseEnMesa = (lobby) => {
		this.setState({
			view: 'MesaView',
			lobby: lobby,
		});
	}

	handleFalloSession = (error) => {
		this.setState({
			error: error,
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
		if (this.state.view === 'EntranceView') {
			return ( <EntranceView app={this}
				url={url}
				entrarAsGuest={this.handleEntrarAsGuest} 
				actualizarJugador={this.actualizarJugador} /> ); 
		}

		const cIdValue = document.cookie.split('; ')
		.find(row => row.startsWith('c_id='))
		.split('=')[1];
		
		if (this.state.view === 'HomeView') {
			return ( <HomeView app={this}
				url={url}
				cId={cIdValue}
				jugador={this.state.jugador}
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

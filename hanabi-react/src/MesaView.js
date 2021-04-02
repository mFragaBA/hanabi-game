import React from 'react'
import io from 'socket.io-client'
import LobbyView from './LobbyView.js'
import JuegoView from './JuegoView.js'


class MesaView extends React.Component {
	constructor(props) {
		super(props)
		this.socket = io(this.props.url);
		this.state = {
			view: 'LobbyView',
			connectionSet: false,
		}
	}

	componentDidMount() {
		this.socket.emit('connection', {"c_id": this.props.cId});
		this.socket.on('connected', () => { this.setState({connectionSet: true}); });
		this.socket.on('partida_iniciada', () => {
			this.handlePartidaIniciada()
		});
		this.socket.on('partida_terminada', () => {
			this.handlePartidaTerminada()
		});
		this.socket.on('disconnect', (reason) => {
			console.log('Desconectado. Motivo:', reason);
			if (reason === 'io server disconnect') {
				// the disconnection was initiated by the server, you need to reconnect manually
				this.socket.connect();
			}
			// else the socket will automatically try to reconnect
		});
	}
	
	handlePartidaIniciada() {
		this.setState({
			view: 'JuegoView',
		});
	}

	render() {
		if (this.state.connectionSet) {
			if (this.state.view === 'LobbyView') {
				return (<div>
						<LobbyView
						app = {this}
						cId={this.props.cId}
						player = {this.props.jugador}
						lobby = {this.props.lobby}
						socket={this.socket}/>
					</div>
				);
			}
			
			if (this.state.view === 'JuegoView') {
				return (<div>
						<JuegoView
						app = {this}
						cId={this.props.cId}
						jugador = {this.props.jugador}
						socket = {this.socket}/>
					</div>
				);
			}

		} else {
			return (<div></div>);
		}
	}
}

export default MesaView;

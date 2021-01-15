import React from 'react'

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
		this.props.socket.on('lobby_update', (data) => {
			this.handleLobbyUpdate(data)
		});
		this.props.socket.emit('estado_lobby_update');
	}

	handleLobbyUpdate(estado) {
		console.log(estado)
		this.setState({
			jugadores: estado['jugadores'],
		});
	}

	render() {
		return (
			<div>
			{this.state.jugadores}
			</div>
		);
	}
}

export default LobbyView;

import React from 'react'

class ListaSeleccionable extends React.Component {
	constructor(props) {
		super(props);
		console.log(props.items);
		this.state = {
			items: props.items,
		};
	}

	static getDerivedStateFromProps(props, prevState) {
		console.log(props.items);
		return {
			items: props.items,
		};
	}

	render() {
		if (this.state.items) {
			return (<ul>
				{this.state.items.map((item, index) =>
					<li key={index} onClick={ () => this.props.accion(item, index)}>
						{item}
					</li>
				)}
				</ul>
			);
		} else {
			return (
				<p>No hay salas disponibles. Intentá creando una e invitá a más jugadores</p>
			);
		}
	}
}

export default ListaSeleccionable;

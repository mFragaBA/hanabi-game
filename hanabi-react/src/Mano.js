import React from 'react';
import Carta from './Carta';

export class Mano extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			jugador: props.jugador,
			cartas: props.mano.cartas,
			pistas: props.mano.pistas,
		};
	}

	componentWillReceiveProps(nextProps) {
		this.setState({
			jugador: nextProps.jugador,
			cartas: nextProps.mano.cartas,
			pistas: nextProps.mano.pistas,
		});
	}

	zIdxFor = (idx) => {
		return "z-" + String(Number(idx) * 10);
	}

	onCartaSeleccion = (index, carta) => {
		this.props.onCartaSeleccion(this.props.jugador, 
			{
				'index': index,
				'Numero': carta[0],
				'Color': carta[1],
			});	
	}

	cartas = () => {
		return (
			<div className="flex flex-row">
				{ this.state.cartas.map((carta, index) =>
					<div className={this.zIdxFor(index)}>
						<Carta numero={carta[0]} color={carta[1]} pistas={this.state.pistas[index]} onCartaSeleccion={this.onCartaSeleccion} key={index} indice={index} margin="-mr-10"/>
					</div>
				) }
			</div>
		);
	}

	render() {
		return (
			<div className="flex flex-col">
				<div className="rounded border border-blue-400 text-right bg-pink-500 bg-opacity-60">
					{this.state.jugador}
				</div>
				{this.cartas()}
			</div>
		)
	}
}

export default Mano;

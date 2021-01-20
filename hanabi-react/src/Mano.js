import React from 'react';
import Carta from './Carta';

class Mano extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			jugador: props.jugador,
			cartas: props.mano.cartas,
			pistas: props.mano.pistas,
		};
	}

	zIdxFor = (idx) => {
		return "z-" + String(Number(idx) * 10);
	}

	render() {
		return (
			<div className="flex flex-col">
				<div className="rounded border border-blue-400 text-right bg-pink-500 bg-opacity-60">
					{this.state.jugador}
				</div>
				<div className="flex flex-row">
					{this.state.cartas.map((carta, index) =>
						<div className={this.zIdxFor(index)}>
							<Carta numero={carta[0]} color={carta[1]} pistas={this.state.pistas[index]} onSelect={this.props.onCardSelection}/>
						</div>
					)}
				</div>
			</div>
		)
	}
}

export default Mano;

import React from 'react';
import Carta from './Carta';

function arraysEqual(a,b) {
    /*
        Array-aware equality checker:
        Returns whether arguments a and b are == to each other;
        however if they are equal-lengthed arrays, returns whether their 
        elements are pairwise == to each other recursively under this
        definition.
    */
    if (a instanceof Array && b instanceof Array) {
        if (a.length!=b.length)  // assert same length
            return false;
        for(var i=0; i<a.length; i++)  // assert each element equal
            if (!arraysEqual(a[i],b[i]))
                return false;
        return true;
    } else {
        return a==b;  // if not both arrays, should be the same
    }
}

export class Mano extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			jugador: props.jugador,
			cartas: props.mano.cartas,
			pistas: props.mano.pistas,
		};
	}

	componentDidUpdate(prevProps) {
		if (!arraysEqual(this.props.cartas, prevProps.cartas) || !arraysEqual(this.props.pistas, prevProps.pistas)) {
			this.setState({
				cartas: this.props.cartas,
				pistas: this.props.pistas,
			});
		}
	}

	zIdxFor = (idx) => {
		return "z-" + String(Number(idx) * 10);
	}

	onCartaSeleccion = (index, carta) => {
		this.props.onCartaSeleccion(this.props.jugador, 
			{
				index: index,
				numero: carta[0],
				color: carta[1],
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

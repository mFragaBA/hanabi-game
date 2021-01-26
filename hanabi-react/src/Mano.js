import React from 'react';
import Carta from './Carta';

export default function Mano(props) {

	let cartas = props.mano.cartas
	let pistas = props.mano.pistas
	let jugador = props.jugador

	let zIdxFor = (idx) => {
		return "z-" + String(Number(idx) * 10);
	}

	let onCartaSeleccion = (index, carta) => {
		props.onCartaSeleccion(jugador, 
			{
				'index': index,
				'Numero': carta[0],
				'Color': carta[1],
			});	
	}

	return (
		<div className="flex flex-col">
			<div className="rounded border border-blue-400 text-right bg-pink-500 bg-opacity-60">
				{jugador}
			</div>
			<div className="flex flex-row">
				{ cartas.map((carta, index) =>
					<div className={zIdxFor(index) + " -mr-10 hover:shadow-red"}>
						<Carta numero={carta[0]} color={carta[1]} pistas={pistas[index]} onCartaSeleccion={onCartaSeleccion} key={index} indice={index}/>
					</div>
				) }
			</div>
		</div>
	)
}


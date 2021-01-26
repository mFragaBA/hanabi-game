import React from 'react';
import Carta from './Carta';

function TiraDeCartas(props) {
	
	let cartas = props.cartas
	let pistas = props.pistas
	let hoverClass = props.hover

	let zIdxFor = (idx) => {
		return "z-" + String(Number(idx) * 10);
	}

	return (
		<div className="flex flex-row">
			{ cartas.map((carta, index) =>
				<div className={zIdxFor(index) + " -mr-8 " + hoverClass}>
					<Carta numero={carta[0]} color={carta[1]} pistas={pistas[index]} onCartaSeleccion={props.onCartaSeleccion} key={index} indice={index}/>
				</div>
			) }
		</div>
	);
}

export default function Mano(props) {

	let cartas = props.mano.cartas
	let pistas = props.mano.pistas
	let jugador = props.jugador

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
			<div className="rounded border border-blue-400 text-right text-xl bg-pink-500 bg-opacity-60">
				{jugador}
			</div>
			<TiraDeCartas cartas={cartas} pistas={pistas} hover={"hover:shadow-red"} onCartaSeleccion={onCartaSeleccion}/>
		</div>
	)
}


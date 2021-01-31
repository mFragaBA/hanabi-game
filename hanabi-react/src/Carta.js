import React from 'react';

import {ReactComponent as CartaAmarilla} from './img/carta_amarilla_token.svg';
import {ReactComponent as CartaAzul} from './img/carta_azul_token.svg';
import {ReactComponent as CartaVerde} from './img/carta_verde_token.svg';
import {ReactComponent as CartaBlanca} from './img/carta_blanca_token.svg';
import {ReactComponent as CartaRoja} from './img/carta_roja_token.svg';


const tokens = {
	Amarillo: CartaAmarilla,
	Azul: CartaAzul,
	Verde: CartaVerde,
	Blanco: CartaBlanca,
	Rojo: CartaRoja,
}

const textColor = {
	Amarillo: "text-yellow-400",
	Azul: "text-blue-400",
	Verde: "text-green-400",
	Blanco: "text-white",
	Rojo: "text-red-400",
}
		
const backColor = {
	Amarillo: "bg-yellow-400",
	Azul: "bg-blue-400",
	Verde: "bg-green-400",
	Blanco: "bg-white",
	Rojo: "bg-red-400",
}

let distribucionColumnasTokens = {
	'1': [1],
	'2': [2],
	'3': [2, 1],
	'4': [2, 2],
	'5': [2, 1, 2],
}

export default function Carta(props) {
	let diseñoCarta = () => {
		let numero = props.numero;
		let color = props.color;

		console.log(numero);
		console.log(color);

		const TokenColor = tokens[color];
		const distribucion = [...distribucionColumnasTokens[numero]];

		return (
			<div className="flex flex-row h-full justify-center">
				{ distribucion.map((item, index) => 
					<div className="flex flex-col flex-grow justify-center" key={index}>
						{ [...Array(item)].map((e, i) => 
							<div className="flex-1 flex-grow max-w-6 max-h-7 relative m-0.5">
								<TokenColor className="absolute top-0 bottom-0" height="100%" width="100%" viewBox="0 0 140 140" preserveAspectRatio="xMidYMid meet" key={i} />
							</div>
						)}
					</div>	
				)}
			</div>
		);
	}

	if (props.numero === 0) {
		return (
			<div className="border-dotted border-4 border-light-blue-500 w-28 h-36 rounded">
				
			</div>
		);
	}
		
	let pistaStr = "?";
	let pistaClassName = "m-0.5 flex-none border rounded text-center text-lg text-black h-8 w-4 ";
	let tieneColor = false;

	props.pistas.forEach(pista => {
		if (pista[0] == "Color") {
			pistaClassName = pistaClassName + backColor[pista[1]];
			tieneColor = true;
		} else if (pista[0] == "Numero") {
			pistaStr = pista[1]; 
		}
	});

	if (!tieneColor) pistaClassName += "bg-pink-400";

	if (props.numero === -1) {
		let cName = "border border-white w-28 h-36 bg-dorso bg-contain rounded text-lg";
		return (
			<div className="flex flex-col items-center">
				<div className={cName} onClick={() => props.onCartaSeleccion(props.indice, [props.numero, props.color])}>
				</div>	
				{props.pistas.length > 0 && 
					<div className={"flex-none " + pistaClassName}>
						{pistaStr}
					</div>
				}
			</div>
		);
	}

	let cName = "border border-white w-28 h-36 flex flex-col bg-carta rounded p-0.5 text-lg";
	return (
		<div className="flex flex-col items-center">
			<div className={cName} onClick={() => props.onCartaSeleccion(props.indice, [props.numero, props.color])}>
				<div className="flex flex-row flex-none">
					<div className={"text-left flex-grow " + textColor[props.color]}>
						{ props.numero }
					</div>
					<div className={"text-right " + textColor[props.color]}>
						{ props.numero }
					</div>
				</div>
				<div className="flex-grow p-1">
					{diseñoCarta()}
				</div>
				<div className="flex flex-row flex-none">
					<div className={"text-left flex-grow " + textColor[props.color]}>
						{ props.numero }
					</div>
					<div className={"text-right " + textColor[props.color]}>
						{ props.numero }
					</div>
				</div>
			</div>
			{props.pistas.length > 0 && 
				<div>
					<div className={"flex-none " + pistaClassName}>
						{pistaStr}
					</div>
				</div>
			}
		</div>
	);

}

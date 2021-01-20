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

let distribucionColumnasTokens = {
	'1': [1],
	'2': [2],
	'3': [2, 1],
	'4': [2, 2],
	'5': [2, 1, 2],
}

class Carta extends React.Component {
	constructor(props) {
		super(props);
	}


	diseñoCarta() {
		let numero = this.props.numero;
		let color = this.props.color;

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

	render() {
		return (
			<div className="border border-blue-700 w-28 h-36 flex flex-col bg-carta rounded -mr-10 p-0.5">
				<div className="flex flex-row flex-none">
					<div className={"text-left flex-grow " + textColor[this.props.color]}>
						{ this.props.numero }
					</div>
					<div className={"text-right " + textColor[this.props.color]}>
						{ this.props.numero }
					</div>
				</div>
				<div className="flex-grow p-1">
					{this.diseñoCarta()}
				</div>
				<div className="flex flex-row flex-none">
					<div className={"text-left flex-grow " + textColor[this.props.color]}>
						{ this.props.numero }
					</div>
					<div className={"text-right " + textColor[this.props.color]}>
						{ this.props.numero }
					</div>
				</div>
			</div>
		);
	}

}

export default Carta;

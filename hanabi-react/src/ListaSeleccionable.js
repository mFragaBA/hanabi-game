import React from 'react'

export default function ListaSeleccionable(props) {
	if (props.items) {
		return (<ul>
			{props.items.map((item, index) =>
				<li key={index} onClick={ () => props.accion(item, index)}>
					{item}
				</li>
			)}
			</ul>
		);
	}
}

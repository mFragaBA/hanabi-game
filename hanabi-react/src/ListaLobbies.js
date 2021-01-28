import React from 'react'

export default function ListaLobbies(props) {
	if (props.lobbies) {
		return (
			<table className="table-fixed w-full max-w-full border-none text-lg text-center">
			<thead>
				<tr className="text-white">
					<th className="w-1/2 bg-gray-700">Nombre</th>
					<th className="w-1/2 bg-green-500">Capacidad</th>
				</tr>
			</thead>
			<tbody>
				{props.lobbies.map((item, index) =>
					<tr className="even:bg-gray-100 odd:bg-gray-200 hover:bg-gray-500 hover:text-white" key={index} onClick={ () => props.accion(item, index)}>
						<td>{item.nombre}</td>
						<td>{item.cantJugadores} / {item.capacidad}</td>
					</tr>
				)}
			</tbody>
			</table>
		);
	} else {
		return (
			<p>No hay salas disponibles. Intentá creando una e invitá a más jugadores</p>
		);
	}
}

import React from 'react'

class EntranceView extends React.Component {
    constructor(props) {
		super(props);
		this.state = {
            usuario: '',
            contraseña: '',
            nombre: '',
            error: null,
		};
    }
    
    handleCambioDeNombre(event) {
		let nombre = event.target.value;
		this.setState({nombre: nombre});
		this.props.actualizarJugador(nombre);
    }

    handleErrorGenSession(error) {
		this.setState({
            error: error,
        });
    }
    
    handleEntrarComoGuest(event) {
        if (this.state.nombre) {
            fetch(this.props.url + '/session')
				.catch(
					(error) => {
						console.log(error);
					}
				)
				.then(response => response.json())
				.then(
					(result) => {
                        document.cookie = "c_id=" + result['session'];
                        this.props.entrarAsGuest();
					},
					(error) => {
						this.handleErrorGenSession(error);
					}
				)
				.catch(error => console.log(error));
        }

    }

	campoInput(titulo, texto, callback) {
		return (
			<div className="flex flex-row justify-center">
				<div className="py-4 ml-4 flex-none w-16 h-16"> {titulo} </div>
				<div className="py-2 flex-grow h-16">
					<input className="border py-2 px-3 text-grey-darkest mx-2 rounded" type="text" value={texto} onChange={callback} /> 
				</div>
		</div>
		)
	}

    render() {
        return (
            <div className="h-full flex flex-col align-center content-center items-center justify-center">
                {this.state.error != null &&
			        <div className="flex flex-col">
			        	<div>
			        		Error generando la sessión. Intentar otra vez, actualizar o limpiar las cookies.
			        	</div>
			        	<div>
			        		Error: {this.state.error}
			        	</div>
                    </div>
                }
                <div className="bg-gray-400 flex flex-row align-center content-center items-stretch">
                    <div className="flex flex-col border-r-2 border-green-600">
                        {this.campoInput("Usuario", this.state.usuario, (event) => { console.log("to be implemented"); } ) }
                        {this.campoInput("Contraseña", this.state.contraseña, (event) => { console.log("to be implemented") } ) }
                        <button type="button" className="flex-initial focus:ring bg-opacity-30border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semiboldhover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent roundedm-2" onClick={(event) => { console.log("To be implemented"); }}>
                            Ingresar 	
                        </button>
                    </div>
                    <div className="flex flex-col border-l-2 border-green-600">
                        {this.campoInput("Nombre", this.state.nombre, (event) => { this.handleCambioDeNombre(event); } ) }
                        <button type="button" className="flex-initial focus:ring bg-opacity-30border-opacity-30 bg-green-300 hover:bg-yellow-500 text-black-400 font-semiboldhover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent roundedm-2" onClick={(event) => { this.handleEntrarComoGuest(event) }}>
                            Ingresar como invitado
                        </button>
                    </div>
                </div>
            </div>
		);
    }

}

export default EntranceView;
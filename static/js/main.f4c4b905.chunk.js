(this["webpackJsonphanabi-react"]=this["webpackJsonphanabi-react"]||[]).push([[0],{41:function(e,t,a){},73:function(e,t,a){},74:function(e,t,a){},75:function(e,t,a){"use strict";a.r(t);var o=a(0),i=a(1),n=a.n(i),s=a(34),r=a.n(s),l=(a(41),a(2)),c=a(3),b=a(5),d=a(4),u=a(35),h=a.n(u),p=(a(73),a(74),function(e){Object(b.a)(a,e);var t=Object(d.a)(a);function a(e){var o;return Object(l.a)(this,a),(o=t.call(this,e)).state={jugador:"",lobby:""},o}return Object(c.a)(a,[{key:"handleCambioDeNombre",value:function(e){var t=e.target.value;this.setState({jugador:t}),this.props.app.setState({jugador:t})}},{key:"handleCambioDeLobby",value:function(e){var t=e.target.value;this.setState({lobby:t}),this.props.app.setState({lobby:t})}},{key:"handleCrearLobbySubmit",value:function(e){e.preventDefault();var t=this.state.jugador,a=this.state.lobby;t&&a&&this.props.socket.emit("crear_lobby",{player_name:t,lobby_name:a})}},{key:"handleMostrarLobbies",value:function(e){e.preventDefault();var t=this.state.jugador;this.state.lobby;t&&this.props.app.setState({view:"ListaLobbiesView"})}},{key:"campoInput",value:function(e,t,a){return Object(o.jsxs)("div",{className:"flex flex-row justify-center",children:[Object(o.jsxs)("div",{className:"py-4 ml-4 flex-none w-16 h-16",children:[" ",e," "]}),Object(o.jsx)("div",{className:"py-2 flex-grow h-16",children:Object(o.jsx)("input",{className:"border py-2 px-3 text-grey-darkest mx-2 rounded",type:"text",value:t,onChange:a})})]})}},{key:"render",value:function(){var e=this;return Object(o.jsxs)("div",{className:"flex flex-col h-full",children:[Object(o.jsx)("div",{className:"h-4/5"}),Object(o.jsx)("div",{className:"flex flex-col font-cursive",children:Object(o.jsx)("div",{className:"",children:Object(o.jsx)("form",{onSubmit:function(t){return e.handleCrearLobbySubmit(t)},children:Object(o.jsxs)("div",{className:"flex flex-row",children:[Object(o.jsxs)("div",{className:"flex-auto bg-opacity-30 border-opacity-30 bg-blue-300 mx-5 font-semibold rounded text-black-400 border border-yellow-500",children:[this.campoInput("Nombre",this.state.jugador,(function(t){e.handleCambioDeNombre(t)})),this.campoInput("Lobby",this.state.lobby,(function(t){e.handleCambioDeLobby(t)}))]}),Object(o.jsxs)("div",{className:"flex-auto flex flex-col",children:[Object(o.jsx)("input",{className:"flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-green-300 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2",type:"submit",value:"Crear Lobby"}),Object(o.jsx)("button",{type:"button",className:"flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2",onClick:function(t){e.handleMostrarLobbies(t)},children:"Ver salas disponibles"})]})]})})})})]})}}]),a}(n.a.Component)),j=function(e){Object(b.a)(a,e);var t=Object(d.a)(a);function a(e){var o;return Object(l.a)(this,a),o=t.call(this,e),console.log(e.items),o.state={items:e.items},o}return Object(c.a)(a,[{key:"render",value:function(){var e=this;return this.state.items?Object(o.jsx)("ul",{children:this.state.items.map((function(t,a){return Object(o.jsx)("li",{onClick:function(){return e.props.accion(t,a)},children:t},a)}))}):Object(o.jsx)("p",{children:"No hay salas disponibles. Intent\xe1 creando una e invit\xe1 a m\xe1s jugadores"})}}],[{key:"getDerivedStateFromProps",value:function(e,t){return console.log(e.items),{items:e.items}}}]),a}(n.a.Component),y=function(e){Object(b.a)(a,e);var t=Object(d.a)(a);function a(e){var o;return Object(l.a)(this,a),(o=t.call(this,e)).handleListaLobbyUpdate=function(e){o.setState({lobbies:e})},o.handleLobbySeleccionado=function(e,t){console.log(e+" - "+t),o.selectedLobby=e},o.state={view:"ListarLobbiesView",lobby:""},o}return Object(c.a)(a,[{key:"componentDidMount",value:function(){this.props.socket.on("lista_lobbies",this.handleListaLobbyUpdate),this.props.socket.emit("listar_lobbies")}},{key:"componentWillUnmount",value:function(){this.props.socket.off("lista_lobbies",this.handleListaLobbyUpdate)}},{key:"handleActualizar",value:function(){this.props.socket.emit("listar_lobbies")}},{key:"handleEntrarALobby",value:function(){if(this.selectedLobby){var e=this.props.app.state.jugador;console.log("p: "+e),this.props.socket.emit("unirse_a_lobby",{player_name:e,lobby_name:this.selectedLobby})}}},{key:"render",value:function(){var e=this;return Object(o.jsxs)("div",{className:"flex flex-row h-full pt-20",children:[Object(o.jsx)("div",{className:"flex-grow mx-20 mb-20 p-10 bg-opacity-30 bg-green-300 border border-yellow-500 rounded",children:Object(o.jsx)(j,{items:this.state.lobbies,accion:this.handleLobbySeleccionado})}),Object(o.jsxs)("div",{className:"flex-none flex flex-col mr-10",children:[Object(o.jsx)("button",{type:"button",className:"flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2",onClick:function(){e.handleEntrarALobby()},children:"Entrar Al Lobby"}),Object(o.jsx)("button",{type:"button",className:"flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2",onClick:function(){e.handleActualizar()},children:"Actualizar"})]})]})}}]),a}(n.a.Component),f=function(e){Object(b.a)(a,e);var t=Object(d.a)(a);function a(e){var o;return Object(l.a)(this,a),(o=t.call(this,e)).handleLobbyUpdate=function(e){console.log(e),o.setState({jugadores:e.jugadores})},o.state={view:"ListarLobbiesView",jugador:e.jugador,lobby:e.lobby,jugadores:[]},o}return Object(c.a)(a,[{key:"componentDidMount",value:function(){this.props.socket.on("lobby_update",this.handleLobbyUpdate),this.props.socket.emit("estado_lobby_update")}},{key:"componentWillUnmount",value:function(){this.props.socket.off("lobby_update",this.handleLobbyUpdate)}},{key:"handleIniciarPartida",value:function(){this.props.socket.emit("iniciar_partida")}},{key:"render",value:function(){var e=this;return Object(o.jsxs)("div",{className:"flex flex-col h-full",children:[Object(o.jsxs)("div",{className:"flex-grow flex flex-col p-5 text-2xl bg-opacity-30 bg-green-300 border border-yellow-500 rounded",children:[Object(o.jsx)("div",{className:"text-center",children:" Jugadores en el Lobby "}),Object(o.jsx)("div",{className:"flex flex-row flex-grow",children:Object(o.jsx)("div",{className:"flex-grow",children:Object(o.jsx)(j,{items:this.state.jugadores,accion:this.handleLobbySeleccionado})})})]}),Object(o.jsx)("div",{className:"flex-none text-center",children:Object(o.jsx)("button",{type:"button",className:"flex-initial focus:ring bg-opacity-30 border-opacity-30 bg-blue-300 hover:bg-yellow-500 text-black-400 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded m-2",onClick:function(){e.handleIniciarPartida()},children:"Iniciar Partida"})})]})}}]),a}(n.a.Component),v=function(e){Object(b.a)(a,e);var t=Object(d.a)(a);function a(e){var o;return Object(l.a)(this,a),(o=t.call(this,e)).actualizarEstadoDelJuego=function(){o.props.socket.emit("estado_juego_update")},o.handleJuegoUpdate=function(){console.log("lleg\xf3 update")},o}return Object(c.a)(a,[{key:"componentWillMount",value:function(){this.props.socket.on("juego_update",this.handleJuegoUpdate),this.props.socket.on("estado_expirado",this.actualizarEstadoDelJuego),this.actualizarEstadoDelJuego()}},{key:"render",value:function(){return Object(o.jsx)("div",{})}}]),a}(n.a.Component),m=h()("https://mFragaBA.github.io:5000/"),x=function(e){Object(b.a)(a,e);var t=Object(d.a)(a);function a(e){var o;return Object(l.a)(this,a),(o=t.call(this,e)).state={view:"HomeView",jugador:"",lobby:""},o}return Object(c.a)(a,[{key:"componentDidMount",value:function(){var e=this;m.on("partida_iniciada",(function(){e.handlePartidaIniciada()})),m.on("partida_terminada",(function(){e.handlePartidaTerminada()})),m.on("unido_a_lobby",(function(t){e.handleEntrarALobby(t)}))}},{key:"handleEntrarALobby",value:function(e){this.setState({view:"LobbyView",lobby:e})}},{key:"handlePartidaIniciada",value:function(){this.setState({view:"JuegoView"})}},{key:"viewMatchingState",value:function(){return"HomeView"===this.state.view?Object(o.jsx)(p,{app:this,socket:m}):"ListaLobbiesView"===this.state.view?Object(o.jsx)(y,{app:this,socket:m}):"LobbyView"===this.state.view?Object(o.jsx)(f,{app:this,player:this.state.player,lobby:this.state.lobby,socket:m}):"JuegoView"===this.state.view?Object(o.jsx)(v,{app:this,player:this.state.player,socket:m}):Object(o.jsxs)("div",{children:["La view es inv\xe1lida (",this.state.view,")"]})}},{key:"render",value:function(){return Object(o.jsx)("div",{className:"h-screen bg-cover bg-hanabi p-20",children:this.viewMatchingState()})}}]),a}(n.a.Component),g=function(e){e&&e instanceof Function&&a.e(3).then(a.bind(null,76)).then((function(t){var a=t.getCLS,o=t.getFID,i=t.getFCP,n=t.getLCP,s=t.getTTFB;a(e),o(e),i(e),n(e),s(e)}))};r.a.render(Object(o.jsx)(n.a.StrictMode,{children:Object(o.jsx)(x,{})}),document.getElementById("root")),g()}},[[75,1,2]]]);
//# sourceMappingURL=main.f4c4b905.chunk.js.map
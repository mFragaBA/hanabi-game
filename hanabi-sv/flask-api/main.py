import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from model.manager import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,
        engineio_logger=True,
        cors_allowed_origins='https://mfragaba.github.io',
        async_mode="gevent")


gamesManager = Manager()

@app.route('/')
def index():
    return "Holo"

@app.route('/time')
def time_api():
    return {'time': time.time()}

"""
@socketio.on('message')
def handle_message(data):
    print('received message:', data)

@socketio.on('json')
def handle_message(json):
    print('received json:', json)

@socketio.on('my_event')
def handle_custom_event(json):
    print('received json:', json)
    #Any values returned from the handler function will be passed to the client as args in the callback function
    return 'one', 2

#can support multiple args
@socketio.on('my_event')
def handle_message(arg1, arg2, arg3):
    print('received args:', arg1, arg2, arg3)
"""

nombre_por_sid = {}
lobby_por_sid = {}

@socketio.on('disconnect')
def handle_disconnect():
    print('+++++++')
    print("Cliente DESCONECTADO:", request.sid)
    jugador = nombre_por_sid[request.sid]
    lobby = gamesManager.sala_de(jugador)
    gamesManager.sacar_jugador(jugador, lobby)

@socketio.on('listar_lobbies')
def handle_listar_lobbies():
    lobbies = gamesManager.listar_lobbies()
    print("Lobbies:", lobbies)
    emit('lista_lobbies', lobbies)

@socketio.on('crear_lobby')
def handle_crear_lobby(data):
    try:
        player_name = data['player_name']
        lobby_name = data['lobby_name']
        
        gamesManager.crear_lobby(lobby_name)
        gamesManager.agregar_jugador(player_name, lobby_name) 

        nombre_por_sid[request.sid] = player_name
        lobby_por_sid[request.sid] = lobby_name

        join_room(lobby_name)
        emit('unido_a_lobby', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('unirse_a_lobby')
def handle_unirse_a_lobby(data):
    try:
        player_name = data['player_name']
        lobby_name = data['lobby_name']
        
        gamesManager.agregar_jugador(player_name, lobby_name) 

        nombre_por_sid[request.sid] = player_name
        lobby_por_sid[request.sid] = lobby_name

        join_room(lobby_name)
        emit('unido_a_lobby')
        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(player_name), room=lobby_name, include_self=False)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('iniciar_partida')
def handle_iniciar_partida():
    try:
        lobby_name = lobby_por_sid[request.sid]
        gamesManager.iniciar_juego_en(lobby_name)

        estado = gamesManager.estado_en(lobby_name)
       
        socketio.emit('partida_iniciada', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('salir_del_lobby')
def handle_salir_del_lobby(data):
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        
        gamesManager.sacar_jugador(player_name, lobby_name) 

        leave_room(lobby_name)
        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(player_name), room=lobby_name)

    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('cortar_partida')
def handle_cortar_partida(data):
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        
        gamesManager.cortar_juego_en(lobby_name) 

        leave_room(lobby_name)
        socketio.emit('partida_terminada', gamesManager.estado_del_lobby_de(player_name), room=lobby_name)

    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('registrar_accion')
def handle_registrar_accion(accion):
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        
        if 'jugador' not in accion or accion['jugador'] != player_name:
            return

        gamesManager.tomar_accion_en(lobby_name, accion)
        
        socketio.emit('estado_expirado', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('estado_juego_update')
def handle_actualizar_estado_juego():
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        
        estado = gamesManager.estado_en(lobby_name)
        
        del estado['estado_jugadores'][player_name]
        emit('juego_update', estado, room=lobby_room)
    
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('estado_lobby_update')
def handle_actualizar_estado_lobby():
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        
        emit('lobby_update', gamesManager.estado_del_lobby_de(player_name))
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

if __name__ == '__main__':
    socketio.run(app)

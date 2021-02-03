import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from model.manager import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,
        logger=True,
        engineio_logger=True,
        cors_allowed_origins=['http://localhost:3000', 'https://mfragaba.github.io'],
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
    #TODO handlear mejor el caso en que la sala se vacíe
    print('+++++++')
    print("Cliente DESCONECTADO:", request.sid)

    if request.sid in nombre_por_sid:
        jugador = (request.sid, nombre_por_sid[request.sid])

        lobby = gamesManager.sala_de(jugador)
        gamesManager.sacar_jugador(jugador, lobby)
        leave_room(lobby)
        socketio.emit('estado_expirado', room=lobby)
        del nombre_por_sid[request.sid]

@socketio.on('listar_lobbies')
def handle_listar_lobbies():
    lobbies = gamesManager.listar_lobbies()
    emit('lista_lobbies', lobbies)

@socketio.on('crear_lobby')
def handle_crear_lobby(data):
    try:
        player_name = data['player_name']
        lobby_name = data['lobby_name']
        jugador = (request.sid, player_name)
 
# TODO: arreglar crear_lobby para que use el nombre del jugador así validamos que el nombre sea válido (la otra es que haya un conectar y se encargue de registrar al jugador con dicho nombre)
#        gamesManager.crear_lobby(lobby_name)
        gamesManager.agregar_jugador(jugador, lobby_name) 

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
        
        jugador = (request.sid, player_name)

        gamesManager.agregar_jugador(jugador, lobby_name) 

        nombre_por_sid[request.sid] = player_name
        lobby_por_sid[request.sid] = lobby_name

        join_room(lobby_name)
        emit('unido_a_lobby')
        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(jugador), room=lobby_name, include_self=False)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('iniciar_partida')
def handle_iniciar_partida():
    try:
        lobby_name = lobby_por_sid[request.sid]
        gamesManager.iniciar_juego_en(lobby_name)

        socketio.emit('partida_iniciada', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('salir_del_lobby')
def handle_salir_del_lobby(data):
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        jugador = (request.sid, player_name)
        
        gamesManager.sacar_jugador(jugador, lobby_name) 

        leave_room(lobby_name)
        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(jugador), room=lobby_name)

    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('cortar_partida')
def handle_cortar_partida(data):
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        jugador = (request.sid, player_name)
        
        gamesManager.cortar_juego_en(lobby_name) 

        leave_room(lobby_name)
        emit('partida_terminada', gamesManager.estado_del_lobby_de(jugador), room=lobby_name)

    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('registrar_accion')
def handle_registrar_accion(accion):
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        jugador = (request.sid, player_name)
        
        if 'jugador' not in accion or accion['jugador'] != player_name:
            return

        gamesManager.tomar_accion_en(lobby_name, accion)
        
        emit('estado_expirado', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('estado_juego_update')
def handle_actualizar_estado_juego():
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        jugador = (request.sid, player_name)
        
        estado = gamesManager.estado_en_partida_de(jugador)
        
        emit('juego_update', estado)
    
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('estado_lobby_update')
def handle_actualizar_estado_lobby():
    try:
        player_name = nombre_por_sid[request.sid]
        lobby_name = lobby_por_sid[request.sid]
        jugador = (request.sid, player_name)
        
        emit('lobby_update', gamesManager.estado_del_lobby_de(jugador))
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)

if __name__ == '__main__':
    socketio.run(app)

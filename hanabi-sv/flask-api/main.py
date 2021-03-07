import time
import uuid
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from model.manager import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app,
        logger=True,
        engineio_logger=True,
        cors_allowed_origins=['http://localhost:3000', 'https://mfragaba.github.io'],
        async_mode="eventlet",
        cookie='client-id')


gamesManager = Manager()
next_id = 0

@app.route('/')
def index():
    return "Holo"

@app.route('/time')
def time_api():
    return {'time': time.time()}

@app.route('/session', methods=['GET'])
def connect():
    global next_id
    print("===============CONECTANDO================")
    next_id = next_id + 1
    return {
        'session': next_id
    }
    
@app.route('/listar_lobbies', methods=['GET'])
def handle_listar_lobbies():
    lobbies = gamesManager.listar_lobbies()
    print("LISTANDO LOBBIES")
    return {'lobbies': lobbies}

@app.route('/crear_lobby', methods=['GET'])
def handle_crear_lobby():
    try:
        print("INTENTO DE CONEXION CON ARGS", request.args)
        player_name = request.args.get('player')
        lobby_name = request.args.get('lobby')
        c_id = request.args.get('c_id')
        jugador = (c_id, player_name)

        # TODO: arreglar crear_lobby para que use el nombre del jugador así validamos que el nombre sea válido (la otra es que haya un conectar y se encargue de registrar al jugador con dicho nombre)
        #        gamesManager.crear_lobby(lobby_name)
        gamesManager.agregar_jugador(jugador, lobby_name) 

        nombre_por_cliente[c_id] = player_name
        lobby_por_cliente[c_id] = lobby_name
        
        return {}, 204
    except Exception as ex:
        emit('error_message', {'error': str(ex)})
        return {'error': str(ex)}, 404

@app.route('/unirse_a_lobby')
def handle_unirse_a_lobby():
    try:
        print("INTENTO DE CONEXION CON ARGS", request.args)
        player_name = request.args.get('player')
        lobby_name = request.args.get('lobby')
        c_id = request.args.get('c_id')
        jugador = (c_id, player_name)

        gamesManager.agregar_jugador(jugador, lobby_name) 

        nombre_por_cliente[c_id] = player_name
        lobby_por_cliente[c_id] = lobby_name

        print("AGREGADO")

        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(jugador), room=lobby_name)
        return {}, 204
    except Exception as ex:
        return {'error': str(ex)}, 404

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

nombre_por_cliente = {}
lobby_por_cliente = {}

@socketio.on('connection')
def handle_connection(data):
    print('+++++++')
    print('Cliente CONECTADO', data)
    print('lobbies', lobby_por_cliente)
    c_id = data['c_id']
    lobby = lobby_por_cliente[c_id]
    join_room(lobby)
    emit('connected')

@socketio.on('disconnect')
def handle_disconnect():
    #TODO handlear mejor el caso en que la sala se vacíe
    print('+++++++')
    print("Cliente DESCONECTADO")
    #print("session:", session)
    #print("current_user", current_user)

    #jugador = (session.get('value', ''), nombre_por_cliente[session.get('value', '')])

    #lobby = gamesManager.sala_de(jugador)
    #gamesManager.sacar_jugador(jugador, lobby)
    #leave_room(lobby)
    #socketio.emit('estado_expirado', room=lobby)
    #del nombre_por_cliente[session.get('value', '')]



@socketio.on('iniciar_partida')
def handle_iniciar_partida(data):
    try:
        print('DATA', data)
        lobby_name = lobby_por_cliente[data['c_id']]
        gamesManager.iniciar_juego_en(lobby_name)

        socketio.emit('partida_iniciada', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('salir_del_lobby')
def handle_salir_del_lobby(data):
    try:
        player_name = nombre_por_cliente[data['c_id']]
        lobby_name = lobby_por_cliente[data['c_id']]
        jugador = (data['c_id'], player_name)
        
        gamesManager.sacar_jugador(jugador, lobby_name) 

        leave_room(lobby_name)
        del lobby_por_cliente[session.get('value', '')]
        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(jugador), room=lobby_name)

    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('cortar_partida')
def handle_cortar_partida(data):
    try:
        player_name = nombre_por_cliente[data['c_id']]
        lobby_name = lobby_por_cliente[data['c_id']]
        jugador = (data['c_id'], player_name)
        
        gamesManager.cortar_juego_en(lobby_name) 

        leave_room(lobby_name)
        emit('partida_terminada', gamesManager.estado_del_lobby_de(jugador), room=lobby_name)

    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('registrar_accion')
def handle_registrar_accion(data):
    try:
        accion = data['accion']
        player_name = nombre_por_cliente[data['c_id']]
        lobby_name = lobby_por_cliente[data['c_id']]
        jugador = (data['c_id'], player_name)
        print('DATA', data)
        print('ACCION', accion)
        print('jugador', jugador)
        print('lobby_name:', lobby_name)
        
        if 'jugador' not in accion or accion['jugador'] != player_name:
            return

        gamesManager.tomar_accion_en(lobby_name, accion)
        
        emit('estado_expirado', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('estado_juego_update')
def handle_actualizar_estado_juego(data):
    try:
        player_name = nombre_por_cliente[data['c_id']]
        lobby_name = lobby_por_cliente[data['c_id']]
        jugador = (data['c_id'], player_name)
        
        estado = gamesManager.estado_en_partida_de(jugador)
        
        emit('juego_update', estado)
    
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('estado_lobby_update')
def handle_actualizar_estado_lobby(data):
    try:
        print('data:', data)
        player_name = nombre_por_cliente[data['c_id']]
        lobby_name = lobby_por_cliente[data['c_id']]
        jugador = (data['c_id'], player_name)
        
        emit('lobby_update', gamesManager.estado_del_lobby_de(jugador))
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on_error_default
def default_error_handler(e):
    print("Error", e)
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)

if __name__ == '__main__':
    socketio.run(app)

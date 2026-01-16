import logging
import os
import time
import uuid
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from model.manager import Manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://mfragaba.github.io", "https://mfragaba.github.io/hanabi-game"]}})
socketio = SocketIO(app,
        logger=True,
        engineio_logger=True,
        cors_allowed_origins=['http://localhost:3000', 'https://mfragaba.github.io'],
        async_mode="eventlet",
        cookie='client-id')


gamesManager = Manager()

@app.route('/')
def index():
    return "Holo"

@app.route('/time')
def time_api():
    return {'time': time.time()}

@app.route('/session', methods=['GET'])
def connect():
    #if "user_id" in request.args:
        # Por ahora no handleamos login
    logger.info("New session requested")
    return {
        'session': uuid.uuid4()
    }
    
@app.route('/listar_lobbies', methods=['GET'])
def handle_listar_lobbies():
    lobbies = gamesManager.listar_lobbies()
    logger.info("Listing lobbies")
    return {'lobbies': lobbies}

@app.route('/crear_lobby', methods=['POST'])
def handle_crear_lobby():
    try:
        data = request.json
        logger.debug("Creating lobby with data: %s", data)
        player_name = data.get('player')
        lobby_name = data.get('lobby')
        c_id = data.get('c_id')
        jugador = (c_id, player_name)

        gamesManager.agregar_jugador(jugador, lobby_name)

        nombre_por_cliente[c_id] = player_name
        lobby_por_cliente[c_id] = lobby_name

        logger.info("Lobby '%s' created by player '%s'", lobby_name, player_name)
        return {}, 204
    except Exception as ex:
        logger.error("Error creating lobby: %s", ex)
        emit('error_message', {'error': str(ex)})
        return {'error': str(ex)}, 400

@app.route('/unirse_a_lobby', methods=['POST'])
def handle_unirse_a_lobby():
    try:
        data = request.json
        logger.debug("Joining lobby with data: %s", data)
        player_name = data.get('player')
        lobby_name = data.get('lobby')
        c_id = data.get('c_id')
        jugador = (c_id, player_name)

        gamesManager.agregar_jugador(jugador, lobby_name)

        nombre_por_cliente[c_id] = player_name
        lobby_por_cliente[c_id] = lobby_name

        logger.info("Player '%s' joined lobby '%s'", player_name, lobby_name)

        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(jugador), room=lobby_name)
        return {}, 204
    except Exception as ex:
        logger.error("Error joining lobby: %s", ex)
        return {'error': str(ex)}, 400

nombre_por_cliente = {}
lobby_por_cliente = {}

@socketio.on('connection')
def handle_connection(data):
    logger.info("Client connected: %s", data.get('c_id'))
    logger.debug("Connection data: %s, current lobbies: %s", data, lobby_por_cliente)
    c_id = data['c_id']
    lobby = lobby_por_cliente[c_id]
    join_room(lobby)
    emit('connected')

@socketio.on('disconnect')
def handle_disconnect():
    # Don't clean up state on disconnect - client may reconnect
    # State cleanup happens explicitly via 'salir_del_lobby' event
    logger.info("Client disconnected")



@socketio.on('iniciar_partida')
def handle_iniciar_partida(data):
    try:
        logger.debug("Starting game with data: %s", data)
        lobby_name = lobby_por_cliente[data['c_id']]
        gamesManager.iniciar_juego_en(lobby_name)

        socketio.emit('partida_iniciada', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('salir_del_lobby')
def handle_salir_del_lobby(data):
    try:
        c_id = data['c_id']
        player_name = nombre_por_cliente[c_id]
        lobby_name = lobby_por_cliente[c_id]
        jugador = (c_id, player_name)

        gamesManager.sacar_jugador(jugador, lobby_name)

        leave_room(lobby_name)
        del lobby_por_cliente[c_id]
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
        logger.debug("Action registered - player: %s, lobby: %s, action: %s", player_name, lobby_name, accion)
        
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
        logger.debug("Lobby state update requested: %s", data)
        player_name = nombre_por_cliente[data['c_id']]
        lobby_name = lobby_por_cliente[data['c_id']]
        jugador = (data['c_id'], player_name)
        
        emit('lobby_update', gamesManager.estado_del_lobby_de(jugador))
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on_error_default
def default_error_handler(e):
    logger.error("Socket error: %s, event: %s, args: %s", e, request.event["message"], request.event["args"])

if __name__ == '__main__':
    socketio.run(app)

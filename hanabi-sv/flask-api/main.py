import time
import uuid
from flask import Flask, render_template, request, session, jsonify
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from model.manager import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app,
        logger=True,
        engineio_logger=True,
        cors_allowed_origins=['http://localhost:3000', 'https://mfragaba.github.io'],
        async_mode="eventlet",
        manage_session=False)


gamesManager = Manager()

class User(UserMixin, object):
    def __init__(self, id=None):
        self.id = id

@login.user_loader
def load_user(id):
    return User(id)

@app.route('/')
def index():
    return "Holo"

@app.route('/time')
def time_api():
    return {'time': time.time()}

@app.route('/session', methods=['GET', 'POST'])
def connect():
    if request.method == 'GET':
        return jsonify({
            'session': session.get('value', ''),
            'user': current_user.id
                if current_user.is_authenticated else 'anonymous' 
        })
    
    data = request.get_json()
    if 'session' in data:
        session['value'] = data['session']
    elif 'user' in data:
        if data['user']:
            login_user(User(data['user'])
        else:
            logout_user()
    else:
        session['value'] = uuid.uuid4()
        login_user(User('Guest #' + session.get('value', '')))
    
    return '', 204

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

@socketio.on('disconnect')
def handle_disconnect():
    #TODO handlear mejor el caso en que la sala se vacíe
    print('+++++++')
    print("Cliente DESCONECTADO:", current_user.id)

    #jugador = (session.get('value', ''), nombre_por_cliente[session.get('value', '')])

    #lobby = gamesManager.sala_de(jugador)
    #gamesManager.sacar_jugador(jugador, lobby)
    #leave_room(lobby)
    #socketio.emit('estado_expirado', room=lobby)
    #del nombre_por_cliente[session.get('value', '')]

@socketio.on('listar_lobbies')
@authenticated_only
def handle_listar_lobbies():
    lobbies = gamesManager.listar_lobbies()
    emit('lista_lobbies', lobbies)

@socketio.on('crear_lobby')
@authenticated_only
def handle_crear_lobby(data):
    try:
        player_name = data['player_name']
        lobby_name = data['lobby_name']
        jugador = (session.get('value', ''), player_name)
 
# TODO: arreglar crear_lobby para que use el nombre del jugador así validamos que el nombre sea válido (la otra es que haya un conectar y se encargue de registrar al jugador con dicho nombre)
#        gamesManager.crear_lobby(lobby_name)
        gamesManager.agregar_jugador(jugador, lobby_name) 

        nombre_por_cliente[session.get('value', '')] = player_name
        lobby_por_cliente[session.get('value', '')] = lobby_name

        join_room(lobby_name)
        emit('unido_a_lobby', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('unirse_a_lobby')
@authenticated_only
def handle_unirse_a_lobby(data):
    try:
        player_name = data['player_name']
        lobby_name = data['lobby_name']
        
        jugador = (session.get('value', ''), player_name)

        gamesManager.agregar_jugador(jugador, lobby_name) 

        nombre_por_cliente[session.get('value', '')] = player_name
        lobby_por_cliente[session.get('value', '')] = lobby_name

        join_room(lobby_name)
        emit('unido_a_lobby')
        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(jugador), room=lobby_name, include_self=False)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('iniciar_partida')
@authenticated_only
def handle_iniciar_partida():
    try:
        lobby_name = lobby_por_cliente[session.get('value', '')]
        gamesManager.iniciar_juego_en(lobby_name)

        socketio.emit('partida_iniciada', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('salir_del_lobby')
@authenticated_only
def handle_salir_del_lobby(data):
    try:
        player_name = nombre_por_cliente[session.get('value', '')]
        lobby_name = lobby_por_cliente[session.get('value', '')]
        jugador = (session.get('value', ''), player_name)
        
        gamesManager.sacar_jugador(jugador, lobby_name) 

        leave_room(lobby_name)
        del lobby_por_cliente[session.get('value', '')]
        socketio.emit('lobby_update', gamesManager.estado_del_lobby_de(jugador), room=lobby_name)

    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('cortar_partida')
@authenticated_only
def handle_cortar_partida(data):
    try:
        player_name = nombre_por_cliente[session.get('value', '')]
        lobby_name = lobby_por_cliente[session.get('value', '')]
        jugador = (session.get('value', ''), player_name)
        
        gamesManager.cortar_juego_en(lobby_name) 

        leave_room(lobby_name)
        emit('partida_terminada', gamesManager.estado_del_lobby_de(jugador), room=lobby_name)

    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('registrar_accion')
@authenticated_only
def handle_registrar_accion(accion):
    try:
        player_name = nombre_por_cliente[session.get('value', '')]
        lobby_name = lobby_por_cliente[session.get('value', '')]
        jugador = (session.get('value', ''), player_name)
        
        if 'jugador' not in accion or accion['jugador'] != player_name:
            return

        gamesManager.tomar_accion_en(lobby_name, accion)
        
        emit('estado_expirado', room=lobby_name)
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('estado_juego_update')
@authenticated_only
def handle_actualizar_estado_juego():
    try:
        player_name = nombre_por_cliente[session.get('value', '')]
        lobby_name = lobby_por_cliente[session.get('value', '')]
        jugador = (session.get('value', ''), player_name)
        
        estado = gamesManager.estado_en_partida_de(jugador)
        
        emit('juego_update', estado)
    
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on('estado_lobby_update')
@authenticated_only
def handle_actualizar_estado_lobby():
    try:
        player_name = nombre_por_cliente[session.get('value', '')]
        lobby_name = lobby_por_cliente[session.get('value', '')]
        jugador = (session.get('value', ''), player_name)
        
        emit('lobby_update', gamesManager.estado_del_lobby_de(jugador))
    except Exception as ex:
        emit('error_message', {'error': str(ex)})

@socketio.on_error_default
@authenticated_only
def default_error_handler(e):
    print("Error", e)
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)

if __name__ == '__main__':
    socketio.run(app)

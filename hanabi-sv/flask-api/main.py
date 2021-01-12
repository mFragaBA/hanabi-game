import time
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


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
@socketio.on('crear_partida')
def handle_crear_partida(data):
    pass

@socketio.on('unirse_a_lobby')
def handle_unirse_a_lobby(data):
    pass

@socketio.on('iniciar_partida')
def handle_iniciar_partida(data):
    pass

@socketio.on('salir_del_lobby')
def handle_salir_del_lobby(data):
    pass

@socketio.on('cortar_partida'):
def handle_cortar_partida(data):
    pass

@socketio.on('registrar_accion'):
def handle_registrar_accion(data):
    pass

@socketio.on('actualizar_estado'):
def handle_actualizar_estado(data):
    pass

if __name__ == '__main__':
    socketio.run(app)

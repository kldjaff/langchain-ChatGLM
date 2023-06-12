from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit , Namespace

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

# @app.route('/')
# def index():
#     return render_template('index.html')

class ChatNamespace(Namespace):
    def on_connect(self):
        print('Client connected')

    def on_disconnect(self):
        print('Client disconnected')

    def on_my_event(self, data):
        self.emit('my_response', {'data': 'got it!'})

socketio.on_namespace(ChatNamespace('/chat'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',debug=True, use_reloader=False)

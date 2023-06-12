from flask import Flask
from flask_sockets import Sockets
import datetime

app = Flask(__name__)
sockets = Sockets(app)

from flask_cors import *
CORS(app, supports_credentials=True)

@sockets.route('/echo')
def echo_socket(ws):
    print("hello")
    while not ws.closed:
        msg = ws.receive()
        print(msg)
        now = datetime.datetime.now().isoformat()
        ws.send(now)  #发送数据

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()

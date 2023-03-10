from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from blocklist import BLOCKLIST
from resources.user import UserRegister, UserLogin, TokenRefresh, UserLogout

from resources.server import Server
from resources.serverstatus import ServerStatus
from resources.servermodems import ServerModems
from resources.servermodem import ServerModem
from resources.servermodem import ServerModemReboot

from flask_socketio import SocketIO, emit
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from random import random
from threading import Thread, Event
from time import sleep

from socketservice.modems import ModemsService
from framework.models.server import ServerModel

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
CORS(app)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='http://localhost:3000')

app.config["JWT_SECRET_KEY"] = "berners"
jwt = JWTManager(app)

api = Api(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    # TODO: Read from a config file instead of hard-coding
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")

api.add_resource(Server, "/server")
api.add_resource(ServerStatus, "/server/status")
api.add_resource(ServerModems, "/server/modem")
api.add_resource(ServerModem, "/server/modem/<int:modem_id>")
api.add_resource(ServerModemReboot, "/server/modem/<int:modem_id>/reboot")


#https://github.com/ajaichemmanam/react-flask-socketio/blob/7cdfe2c76a8ad4eb36e097dd30e2b273882a08fb/server.py

server_model = ServerModel.find_by_id(1)

global modems_status_thread
global modems_details_thread

modems_status_thread = Thread()
modems_status_thread_stop_event = Event()

class ModemsStatusThread(Thread):
    def __init__(self):
        self.delay = 1
        super(ModemsStatusThread, self).__init__()

    def run_forever(self):        
        modems_service = ModemsService(server_model = server_model)
        try:
            while not modems_status_thread_stop_event.isSet():
                modems = modems_service.modems_status()
                socketio.emit('modems', modems, broadcast=True)
                sleep(self.delay)

        except KeyboardInterrupt:
            # kill()
            pass

    def run(self):
        self.run_forever()


modems_details_thread = Thread()
modems_details_thread_stop_event = Event()

class ModemsDetailsThread(Thread):
    def __init__(self):
        self.delay = 1
        super(ModemsDetailsThread, self).__init__()

    def run_forever(self):        
        modems_service = ModemsService(server_model = server_model)
        try:
            while not modems_details_thread_stop_event.isSet():
                modems = modems_service.modems_status()
                socketio.emit('modems_details', modems, broadcast=True)
                sleep(self.delay)

        except KeyboardInterrupt:
            # kill()
            pass

    def run(self):
        self.run_forever()


@socketio.on('connect')
def connect():
    print('someone connected to websocket')
    emit('message', {'text': 'You are connected to socket.io'})

    # global modems_status_thread
    # if not modems_status_thread.is_alive():
    #     print("Starting ModemsStatusThread")
    #     modems_status_thread = ModemsStatusThread()
    #     modems_status_thread.start()

    # global modems_details_thread
    # if not modems_details_thread.is_alive():
    #     print("Starting ModemsDetailsThread")
    #     modems_details_thread = ModemsDetailsThread()
    #     modems_details_thread.start()

# Handle the webapp connecting to the websocket, including namespace for testing
# @socketio.on('connect', namespace='/devices')
# def test_connect2():
#     print('someone connected to websocket!')
#     emit('responseMessage', {'data': 'Connected devices! ayy'})

# Handle the webapp sending a message to the websocket
# @socketio.on('message')
# def handle_message(message):
#     # print('someone sent to the websocket', message)
#     print('Data', message["data"])
#     print('Status', message["status"])
#     global thread
#     global thread_stop_event
#     if (message["status"]=="Off"):
#         if thread.isAlive():
#             thread_stop_event.set()
#         else:
#             print("Thread not alive")
#     elif (message["status"]=="On"):
#         if not thread.isAlive():
#             thread_stop_event.clear()
#             print("Starting Thread")
#             thread = ModemsThread()
#             thread.start()
#     else:
#         print("Unknown command")


# # Handle the webapp sending a message to the websocket, including namespace for testing
# @socketio.on('message', namespace='/devices')
# def handle_message2():
#     print('someone sent to the websocket!')


@socketio.on_error_default
def default_error_handler(e):
    print(e)

if __name__ == '__main__':
    # socketio.run(app=app, port=5000)
    if not modems_status_thread.is_alive():
        print("Starting ModemsStatusThread")
        modems_status_thread = ModemsStatusThread()
        modems_status_thread.start()

    if not modems_details_thread.is_alive():
        print("Starting ModemsDetailsThread")
        modems_details_thread = ModemsDetailsThread()
        modems_details_thread.start()

    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

    # global modems_status_thread
    # if not modems_status_thread.is_alive():
    #     print("Starting ModemsStatusThread")
    #     modems_status_thread = ModemsStatusThread()
    #     modems_status_thread.start()

    # # global modems_details_thread
    # if not modems_details_thread.is_alive():
    #     print("Starting ModemsDetailsThread")
    #     modems_details_thread = ModemsDetailsThread()
    #     modems_details_thread.start()
import sys
sys.path.append("../")
from framework.service.modem.modemservice import ModemState
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.modem import ModemDiagnose, ModemLockWizardStepResponse, ModemReboot, ModemRotate, ModemScheduleAutoRotate, Modems, Modem, ModemLogs
from resources.proxyuser import ProxyUserByUsername, ProxyUserModemFilters, ProxyUsers
from blocklist import BLOCKLIST
from resources.user import UserRegister, UserLogin, TokenRefresh, UserLogout
from resources.server import Server, ServerUSBPorts
from resources.serverstatus import ServerStatus
from flask_socketio import SocketIO, emit
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from threading import Thread, Lock
from app import app

async_mode = None

app.instance = Flask(__name__)
app.instance.config["PROPAGATE_EXCEPTIONS"] = True
CORS(app.instance)

app.instance.config['SECRET_KEY'] = 'secret!'
app.socketio = SocketIO(app.instance, async_mode=async_mode, cors_allowed_origins='*')

app.instance.config["JWT_SECRET_KEY"] = "berners"
jwt = JWTManager(app.instance)

api = Api(app.instance)

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
api.add_resource(ServerUSBPorts, "/server/usb-ports")

api.add_resource(Modems, "/modem")
api.add_resource(Modem, "/modem/<int:modem_id>")
api.add_resource(ModemReboot, "/modem/<int:modem_id>/reboot")
api.add_resource(ModemRotate, "/modem/<int:modem_id>/rotate")
api.add_resource(ModemDiagnose, "/modem/<int:modem_id>/diagnose")
api.add_resource(ModemLockWizardStepResponse, "/modem/<int:modem_id>/lock/<string:lock_id>/wizard/step/<string:step_id>/response")
api.add_resource(ModemLogs, "/modem/<int:modem_id>/log")
api.add_resource(ModemScheduleAutoRotate, "/modem/<int:modem_id>/schedule/auto-rotate")

api.add_resource(ProxyUsers, "/proxy-users")
api.add_resource(ProxyUserByUsername, "/proxy-user/by-username/<string:username>")
api.add_resource(ProxyUserModemFilters, "/proxy-user/<int:proxy_user_id>/modem/<int:modem_id>/filters")

#https://github.com/ajaichemmanam/react-flask-socketio/blob/7cdfe2c76a8ad4eb36e097dd30e2b273882a08fb/server.py

modems_status_thread = None
modems_status_thread_lock = Lock()
def background_thread_modems_status():
    while True:
        modems = app.modems_service.modems_observer.observe_status()        
        app.socketio.emit('modems', ModemState.schema().dump(modems, many=True), broadcast=True)
        thread = Thread(target=app.modems_service.modems_observer.observe_connectivity)
        thread.start()
        app.socketio.sleep(1)

modems_auto_rotate_thread = None
modems_auto_rotate_thread_lock = Lock()
def background_thread_modems_auto_rotate():
    while True:
        app.modems_auto_rotate_service.check_and_rotate()
        app.socketio.sleep(1)

@app.socketio.event
def connect():
    print('socketio: client connected')

@app.socketio.on_error_default
def default_error_handler(e):
    print(e)

if __name__ == '__main__':
    #http_server = WSGIServer(('',5000), app.instance, handler_class=WebSocketHandler)
    #http_server.serve_forever()   

    with modems_status_thread_lock:
        if modems_status_thread is None:
            modems_status_thread = app.socketio.start_background_task(background_thread_modems_status)

    with modems_auto_rotate_thread_lock:
        if modems_auto_rotate_thread is None:
            modems_auto_rotate_thread = app.socketio.start_background_task(background_thread_modems_auto_rotate)

    app.socketio.run(app=app.instance, port=5000, host='0.0.0.0')
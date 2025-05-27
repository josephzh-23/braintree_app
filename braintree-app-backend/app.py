import eventlet
eventlet.monkey_patch()
# Force select hub (more stable on macOS) a patch
import eventlet.hubs
eventlet.hubs.use_hub('selects')


from flask import Flask
from flask_cors import CORS
from config import configure_braintree, setup_dynamodb

from redis_client import socketio
from payments_routes import payment_routes
from user_routes import user_routes
app = Flask(__name__)

CORS(app)


app.config['SECRET_KEY'] = 'secret!'

# Use Redis for message queue if needed (for scaling across servers)
# socketio = SocketIO(app, cors_allowed_origins="*", message_queue='redis://localhost:6379')
socketio.init_app(app, cors_allowed_origins="*")

'''
Step 2: to register the socket event then do 
'''
import chat

configure_braintree()
setup_dynamodb()

# start_listener()

# Register blueprints
app.register_blueprint(payment_routes)
app.register_blueprint(user_routes)


if __name__ == '__main__':
    print("Server started")
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True)

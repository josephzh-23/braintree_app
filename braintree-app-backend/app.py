import uuid
from datetime import datetime
from uuid import UUID


# Used for preventing circular dependency here
import eventlet
eventlet.monkey_patch()
from extensions import db

# Force select hub (more stable on macOS) a patch
import eventlet.hubs
eventlet.hubs.use_hub('selects')


from flask import Flask
from flask_cors import CORS
from config import configure_braintree, setup_dynamodb

from redis_client import socketio
from payments_routes import payment_routes
from user_routes_postgresql import user_routes
# from user_routes import user_routes



'''
Step 2: to register the socket event then do 
'''

configure_braintree()
setup_dynamodb()

from extensions import db

def create_app():
    print("the app has started")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:940108Cool!@database-1.cwvoqeyo066c.us-east-1.rds.amazonaws.com:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    CORS(app)

    app.config['SECRET_KEY'] = 'secret!'

    # Use Redis for message queue if needed (for scaling across servers)
    # socketio = SocketIO(app, cors_allowed_origins="*", message_queue='redis://localhost:6379')
    socketio.init_app(app, cors_allowed_origins="*")


    # Import routes after db is initialized
    from user_routes_postgresql import user_routes
    app.register_blueprint(user_routes)
    app.register_blueprint(payment_routes)
    with app.app_context():
        db.create_all()
    return app





if __name__ == '__main__':
    app = create_app()
    print("Server started")
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True)

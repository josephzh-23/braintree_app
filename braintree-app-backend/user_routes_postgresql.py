import uuid
from datetime import datetime

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UUID
from extensions import db
user_routes = Blueprint('user_routes', __name__)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@user_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    print("i came here")
    if not all([username, email, password]):
        return jsonify({'error': 'Missing fields'}), 400

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 409

    # Hash the password, we will skip here
    hashed_pw = password

    new_user = User(
        username=username,
        email=email,
        password=hashed_pw
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'user_id': str(new_user.id), 'message': 'User registered successfully'})
from datetime import datetime, timedelta

from flask import Blueprint, jsonify
import uuid
from botocore.exceptions import ClientError
from flask import Flask, request, jsonify
import jwt
import boto3
from werkzeug.security import check_password_hash


'''
Design here:
user:{user_id} => socket_id
room:{room_name} => set of user_ids

WIll use redis here, we need to revamp everything kind of 
'''
user_routes = Blueprint('user_routes', __name__)


# Initialize DynamoDB (optional: use local or AWS profile)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
client = boto3.client('dynamodb', region_name='us-east-1')


user_table_name = 'users'
user_table = dynamodb.Table(user_table_name)




@user_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('username')
    email = data.get('email')
    password = data.get('password')


    ensure_users_table_exists()
    print("i came here asdf")
    if not all([ name, email, password]):
        return jsonify({'error': 'Missing fields'}), 400

    # ✅ Query DynamoDB for existing email
    response = user_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('email').eq(email)
    )
    if response['Items']:
        return jsonify({'error': 'Email already exists'}), 409

    # Generate user_id
    user_id = str(uuid.uuid4())

    # Store to DynamoDB
    user_table.put_item(Item={
        'user_id': user_id,
        'user_name': name,
        'email': email,
        'password': password,  # NOTE: In production, hash this!
        'created_at': datetime.utcnow().isoformat()
    })

    return jsonify({'user_id': user_id, 'message': 'User registered successfully'})



# Simulated DynamoDB table
TABLE_NAME = 'users'
users_table = dynamodb.Table(TABLE_NAME)

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email= data.get('email')
    password = data.get('password')
    print('email is', email)
    # Look up user in DynamoDB using scan, since email is not part of the primary key
    response = users_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('email').eq(email)
    )
    print("user is", response)

    user = response.get('Items')[0]
    if not user or (user.get('password') != password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Create JWT token
    token = jwt.encode({
        'user_id': user.get('user_id'),
        'username': user.get('username'),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, 'secret-key', algorithm='HS256')

    return jsonify({'token': token, 'user_id': user.get('user_id')})


def ensure_users_table_exists():
    try:
        existing_tables = client.list_tables()['TableNames']
        if TABLE_NAME in existing_tables:
            print(f"✅ Table '{TABLE_NAME}' already exists.")
            return dynamodb.Table(TABLE_NAME)
        else:
            print(f"⚙️ Creating table '{TABLE_NAME}'...")
            table = dynamodb.create_table(
                TableName=TABLE_NAME,
                KeySchema=[
                    {'AttributeName': 'user_id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'user_id', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'  # Use 'PROVISIONED' if you want to specify capacity
            )
            table.wait_until_exists()
            print(f"✅ Table '{TABLE_NAME}' created successfully.")
            return table
    except ClientError as e:
        print(f"❌ Error checking/creating table: {e}")
        return None
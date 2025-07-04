
from flask import Flask, jsonify
import boto3
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # Change to your region
users_table = dynamodb.Table('users')


@app.route('/available-users', methods=['GET'])
def get_available_users():
    try:
        # Scan for users with status == "available"
        response = users_table.scan(
            FilterExpression=Attr('status').eq('available')
        )
        users = response.get('Items', [])
        print("here are all the users i have ")
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


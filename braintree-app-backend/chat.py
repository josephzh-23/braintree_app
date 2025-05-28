from datetime import datetime

import boto3
from flask import request
from flask_socketio import emit, join_room, leave_room

from redis_client import redis_client, socketio

# and setup for the table here
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
message_table = dynamodb.Table('message')


'''
We need a id for an admin user here, which should be maria 
'''
@socketio.on('connect')
def handle_connect():

    print("client connected: ", request.sid);
    print('🟢 A user connected')

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid

    # Find user by sid
    for key in redis_client.scan_iter("user:*"):

        '''
        We need to delete the user sid 
        '''
        if redis_client.get(key) == sid:
            user_id = key.split(":")[1]
            redis_client.delete(key)

            # Remove from all rooms
            for room_key in redis_client.scan_iter("room:*"):
                redis_client.srem(room_key, user_id)

            break

@socketio.on('join')
def on_join(data):

    username = data['username']
    room = data['room']

    user_id = data['user_id']
    sid = request.sid

    join_room(room)

    '''
    user_id -> sid
    room -> [user_id] 
    '''

    if user_id is None:
        user_id = "83a7590a-41c6-4506-a386-4bf44295c076"
    print("i came here")
    redis_client.set(f"user:{user_id}", sid)
    redis_client.sadd(f"room:{room}", user_id)
    socketio.emit('message', {
        'user': 'System',
        'msg': f"{username} has joined the room."
    }, room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', {'user': 'System', 'msg': f"{username} has left the room."}, room=room)

@socketio.on('send_message')
def send_message(data):
    room = data['room']
    message = data['msg']
    user_id = data['user_id']

    print("the message is", message)
    # Fetch other users in the room
    users_in_room = redis_client.smembers(f"room:{room}")
    if user_id is None:
        user_id = "83a7590a-41c6-4506-a386-4bf44295c076"


    socketio.emit('message', {
        'user': user_id,
        'msg': message
    }, room=room)
    message_table.put_item(Item={
        'messageid': 1,
        'userIds': ['user1', 'user2'],
        'string_id': 42,
        'creation_date': datetime.utcnow().isoformat(),
        'content': message
    })


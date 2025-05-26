import threading
import boto3
import time

'''
This listens to our messages here 

'''
sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/008872613422/personal-queue'

def process_message(message):
    print("Message received:", message['Body'])

def listen_to_sqs():
    print("Starting SQS listener...")
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )
            for message in response.get('Messages', []):
                process_message(message)
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        except Exception as e:
            print("Error:", e)
        time.sleep(2)

def start_listener():
    threading.Thread(target=listen_to_sqs, daemon=True).start()
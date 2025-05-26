
from dotenv import load_dotenv
import os

load_dotenv()  # load from .env file

BRAINTREE_MERCHANT_ID = os.getenv('BRAINTREE_MERCHANT_ID')
BRAINTREE_PUBLIC_KEY = os.getenv('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = os.getenv('BRAINTREE_PRIVATE_KEY')
BRAINTREE_ENVIRONMENT = os.getenv('BRAINTREE_ENVIRONMENT')
region = 'us-east-1'
table_name = 'transactions'

braintree_keys = {
    'merchant_id': BRAINTREE_MERCHANT_ID,
    'public_key': BRAINTREE_PUBLIC_KEY,
    'private_key': BRAINTREE_PRIVATE_KEY,
}

import braintree
import boto3

def configure_braintree():
    braintree.Configuration.configure(
        environment=getattr(braintree.Environment, BRAINTREE_ENVIRONMENT.capitalize()),
        merchant_id=BRAINTREE_MERCHANT_ID,
        public_key=BRAINTREE_PUBLIC_KEY,
        private_key=BRAINTREE_PRIVATE_KEY
    )

def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # You can also handle table creation here if needed
    return dynamodb

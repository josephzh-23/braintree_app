from flask import Blueprint, request, jsonify
import braintree
import boto3
from datetime import datetime

payment_routes = Blueprint('payment_routes', __name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
transactions_table = dynamodb.Table('transactions')

@payment_routes.route('/client_token', methods=['GET'])
def client_token():
    token = braintree.ClientToken.generate()
    return jsonify({'token': token})

@payment_routes.route('/checkout', methods=['POST'])
def create_purchase():
    nonce = request.form.get('payment_method_nonce')
    amount = request.form.get('amount')

    result = braintree.Transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        transaction_id = result.transaction.id

        transactions_table.put_item(Item={
            "transaction_id": transaction_id,
            "amount": amount,
            "status": result.transaction.status,
            "created_at": datetime.utcnow().isoformat(),
            "userId": "123",
        })

        return jsonify({"success": True, "transaction_id": transaction_id})
    else:
        return jsonify({"success": False, "error": str(result.message)}), 400
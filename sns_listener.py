import json
import os
import requests
import boto3
from flask import Flask, request, jsonify
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_structured

app = Flask(__name__)

@app.route('/sns-listener', methods=['POST'])
def sns_listener():
    message = json.loads(request.data)
    print("Received SNS message:", message)
    sys.stdout.flush()

    # Handle subscription confirmation
    if message.get('Type') == 'SubscriptionConfirmation' and 'SubscribeURL' in message:
        subscribe_url = message['SubscribeURL']
        response = requests.get(subscribe_url)
        if response.status_code == 200:
            print("Subscription confirmed.")
            sys.stdout.flush()
            return jsonify({'status': 'subscription confirmed'}), 200
        else:
            print("Failed to confirm subscription.")
            sys.stdout.flush()

    # Print the message
    if message.get('Type') == 'Notification':
        print("Message body:", message.get('Message'))
        sys.stdout.flush()
        return jsonify({'status': 'message received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

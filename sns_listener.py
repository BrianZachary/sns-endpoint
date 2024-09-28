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
    print("Received SNS message:" message)

    # Handle subscription confirmation
    if message.get('Type') == 'SubscriptionConfirmation' and 'SubscribeURL' in message:
        subscribe_url = message['SubscribeURL']
        response = requests.get(subscribe_url)
        if response.status_code == 200:
            print("Subscription confirmed.")
        else:
            print("Failed to confirm subscription.")
        return jsonify({'status': 'subscription confirmed'}), 200


    # Create a CloudEvent
    attributes = {
        "type": "com.amazon.sns.message",
        "source": "aws:sns",
    }
    data = {
        "message": message
    }
    event = CloudEvent(attributes, data)

    # Convert CloudEvent to structured format
    headers, body = to_structured(event)

    # Get the K_SINK endpoint from the environment variable
    k_sink = os.getenv('K_SINK')
    if not k_sink:
	print("K_SINK not set")
        return jsonify({'error': 'K_SINK environment variable not set'}), 500

    # Post the CloudEvent to the K_SINK endpoint
    print("K_SINK is", k_sink)
    response = requests.post(k_sink, headers=headers, data=body)
    if response.status_code != 200:
	print("Failed to post CloudEvent")
	print("Headers:", headers)
	print("Data:", body)
        return jsonify({'error': 'Failed to post CloudEvent'}), 500

    print("Successfully posted CloudEvent")
    print("Headers:", headers)
    print("Data:", body)
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify
import boto3
import json

app = Flask(__name__)

# Initialize the SNS client
sns_client = boto3.client('sns', region_name='us-east-2')

@app.route('/sns-listener', methods=['POST'])
def sns_listener():
    # Parse the incoming SNS message
    message_type = request.headers.get('x-amz-sns-message-type')
    message = request.get_json()

    # Handle subscription confirmation
    if message_type == 'SubscriptionConfirmation':
        # Confirm the subscription
        token = message['Token']
        topic_arn = message['TopicArn']
        sns_client.confirm_subscription(TopicArn=topic_arn, Token=token)
        print(f"Subscription confirmed for topic {topic_arn}")
    elif message_type == 'Notification':
        # Print the SNS message
        print(f"Message received: {json.dumps(message, indent=2)}")

    return jsonify({'status': 'success'}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

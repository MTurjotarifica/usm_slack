import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

from dotenv import load_dotenv
from threading import Thread

import json

# Functions to import 
from Imports.importFunction import *

load_dotenv()


# Initialize the Flask app and the Slack app
app = Flask(__name__)
slack_app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

client = slack_app.client

@app.route('/slack/interactive-endpoint', methods=['GET','POST'])
def interactive_trigger():

    data = request.form
    data2 = request.form.to_dict()
    channel_id = json.loads(data2['payload'])['container']['channel_id']
    text = data.get('text')

    response_url = json.loads(data2['payload'])['response_url']
    action_id = json.loads(data2['payload'])['actions'][0]['action_id']

    if action_id == "trend-select":
        payload = json.loads(data2['payload'])
        selected_options = payload['actions'][0]['selected_options']
        selected_values = [option['value'] for option in selected_options]

        thr = Thread(target=backgroundworker_zenserp_trends, args=[client, text, response_url, channel_id, selected_values])
        thr.start()
        
        
    else:
        client.chat_postMessage(channel=channel_id, text="Error: Please try again with different values.")
        
    return 'interactive trigger works', 200

@app.route('/trendz', methods=['POST'])
def trend_route():
    return zenserp_trends(client,trend_block)


@app.route("/helloUSMSLACK", methods=["POST"])
def handle_hello_request():
    data = request.form
    channel_id = data.get('channel_id')
    # Execute the /hello command function
    slack_app.client.chat_postMessage(response_type= "in_channel", channel=channel_id, text="it works!", )
    client.chat_postMessage(response_type= "in_channel", channel=channel_id, text=" 2nd it works!33!", )
    return "Hello world1" , 200


handler = SlackRequestHandler(slack_app)
@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    app.run(debug=True)

import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

from dotenv import load_dotenv


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
    return intTrigger(client, backgroundworker_zenserp_trends)


@app.route('/trendz', methods=['POST'])
def trend_route():
    trend_blocks = generate_trend_block()
    return zenserp_trends(client,trend_blocks)


@app.route("/helloUSMSLACK", methods=["POST"])
def hellousm():
    return handle_hello_request(client)


handler = SlackRequestHandler(slack_app)
@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    app.run(debug=True)

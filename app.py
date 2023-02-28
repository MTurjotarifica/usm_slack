from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['POST'])
def hello():
    return jsonify(
        response_type='in_channel',
        text='Hello, world!'
    )

if __name__ == '__main__':
    app.run()


# from slack_bolt import App

# app = App(
#     token="xoxb-4518285042001-4849883286583-Q1pgXmXv0ByEHK0uDaIZWUh9",
#     signing_secret="48ca0ae53445fc87753ef2a4fb367a5b"
# )

# @app.command("/hello")
# def handle_hello_command(ack, respond):
#     ack()
#     respond("Hello world!")

# if __name__ == "__main__":
#     app.start(port=3000)
#     # app.start(port=int(os.environ.get("PORT", 3000)))


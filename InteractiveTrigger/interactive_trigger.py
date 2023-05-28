from flask import Flask, request
import json
from threading import Thread

def intTrigger(client, backgroundworker_zenserp_trends):
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
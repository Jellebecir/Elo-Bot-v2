import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from multiprocessing import Process
from bot import EloBot

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

bot = EloBot()

@slack_event_adapter.on('member_joined_channel')
def member_joined_channel_event(payload):
    bot.handle_member_joined(payload)

@app.route('/beatme', methods=['POST'])
def handle_beatme_event():
    request_data = request.form
    Process(
        target=bot.handle_match,
        args=(request_data,)
    ).start()
    return Response(), 202

if __name__ == '__main__':
    app.run(debug=True)




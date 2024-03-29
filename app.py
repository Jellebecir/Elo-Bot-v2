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
def handle_beatme_request():
    request_data = request.form
    Process(
        target=handle_beatme_process,
        args=(request_data,)
    ).start()
    return Response(), 202

def handle_beatme_process(request_data):
    bot.handle_beatme(request_data)

@app.route('/leaderboard', methods=['POST'])
def handle_leaderboard_request():
    request_data = request.form
    Process(
        target=handle_leaderboard_process,
        args=(request_data,)
    ).start()
    return Response(), 200

def handle_leaderboard_process(request_data):
    bot.handle_leaderboard(request_data)

@app.route('/score', methods=['POST'])
def handle_score_request():
    request_data = request.form
    Process(
        target=handle_score_process,
        args=(request_data,)
    ).start()
    return Response(), 200

def handle_score_process(request_data):
    bot.handle_score(request_data)

@app.route('/revert', methods=['POST'])
def handle_revert_request():
    request_data = request.form
    Process(
        target=handle_revert_process,
        args=(request_data,)
    ).start()
    return Response(), 200

def handle_revert_process(request_data):
    bot.handle_revert(request_data)

@app.route('/history', methods=['POST'])
def handle_history_request():
    request_data = request.form
    Process(
        target=handle_history_process,
        args=(request_data,)
    ).start()
    return Response(), 200

def handle_history_process(request_data):
    bot.handle_history(request_data)

if __name__ == '__main__':
    app.run(debug=True)




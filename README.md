# Elo-Bot-v2
Slack bot used to keep track of 2 player games with a binary outcome and gives a rating based on the elo system.

# Setup
How to setup the development environment of Elo-Bot

## Prerequisites
 - Python 3.11.x
 - Local MySQL server. For this app to run locally, you need to setup a MySQL serve with a database. You won't need to set up any tables or anything as the app does this for you.

## Environment variables
This app requires a few environment variables that you need to configure for yourself.
### Slack related environment variables
- SLACK_TOKEN - you can find this on your slack app page under `OAUTH & Permissions`
- SIGNING_SECRET - you can find this on your slack app page under `Basic information`
- BOT_ID - I'm pretty sure you can find this _somewhere_ on the slack app page but if you struggle to find it like I did you can follow
[these](https://stackoverflow.com/questions/54466903/how-can-a-slack-bot-find-out-its-own-id) instructions.

### Database related variables
These should be self explanitory, if not, these variables are used to connect to your MySQL server that is required to run this app.
- HOST
- USER
- PASSWORD
- PORT
- DATABASE

## Creating a virtual environment
This project requires a python virtual environment. You can set this up by running `python -m venv .venv`. After this run `pip install -r requirements.txt` to install all required packages for this project.

## Starting test server
[NGROK](https://ngrok.com/) is required to handle web traffic (slack events and bot commands). If not already installed click the provided link to the NGROK website.

Now run the ngrok.exe file and type `ngrok http 5000`. In the terminal, it will say that it's forwarding an ngrok adress to your local flask server. Copy this ngrok adress, go to the event subscription tab of the [slack app webpage](https://api.slack.com/apps), and paste it in the request url appended with `/slack/events` e.g. `https://16ea-82-174-48-158.ngrok-free.app/slack/events`. This also applies to the slash command request urls.

Once this is installed and running, open a new terminal in the project root and run `python app.py`. In the terminal you will see on which port the Flask server is running. For development it will probably say something along the lines of http://127.0.0.1:5000, meaning it's running on port 5000.

**Make sure NGROK is running on the same port as app.y**

It's important to note that, when the ngrok server needs to be reset, you'll receive a different forwarding adress and it needs to be set again in the slack app page.



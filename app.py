import os
from flask import Flask, render_template, request
from flask_cors import CORS
from ConnectStorageAccount import *
from Speech import recognize_from_microphone
from AudioModules import ffmpeg_convert
from ChatGPT import *
from LoginOrRegister import add_username, login_username


os.system('apt update && apt install ffmpeg -y')
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    print('Login page')
    credentials = request.json
    result = login_username(credentials['username'], credentials['password'])
    if result:
        return {'user': credentials['username']}
    return render_template('index.html'), 401


@app.route('/register', methods=['POST'])
def register():
    print('Register page')
    credentials = request.json
    add_username(credentials['username'], credentials['password'])
    return render_template('index.html')


@app.route('/recordsound', methods=['GET'])
def recordsound():
    print('recordsound page')
    return render_template('recordsound.html')


@app.route('/upload_audio', methods=['POST', 'GET'])
def upload_audio():
    user = request.args.get('username')
    # Try and get data from SA, if it exists
    msg_history = get_chat_history(user)

    # Get audio from client
    audio_file = request.files['audio']
    # Convert to wav and save file
    output_filename = ffmpeg_convert(audio_file)
    # Transform to text
    text_msg = recognize_from_microphone(output_filename)
    # Remove wav file from local machine
    os.remove(output_filename)
    # print(text_msg)
    # Send user message with history of conversation to chatGPT and parse response
    if text_msg:
        ai_response, msg_history = send_msg_with_history(text_msg, msg_history)
        # Save complete conversation
        save_chat_history(user, msg_history)
        # print(ai_response)
        return {'yourMessage': 'You: ' + text_msg, 'aiMessage': 'AI Deity: ' + ai_response}
    return {'message': 'Failed to transform speech to text'}


if __name__ == '__main__':
    app.run()

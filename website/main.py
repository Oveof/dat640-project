START_PORT = 8000

import sqlite3
from flask import Flask, request, jsonify , render_template, session
import socket
from waitress import serve
import io
from db import clear_playlist, list_playlist, playlist_add_song, playlist_remove_song, new_user
import string
import random

import numpy as np


def render_playlist(playlist: list[tuple[str,str]]) -> str:
    if playlist == None:
        return ""
    html = ""
    html += "<ul>"
    for song, artist in playlist:
        html += f"<li>{song} - {artist}</li>"

    html += "</ul>"
    html += "</div>"
    return html

def bind_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = START_PORT
    while True:
        try:
            s.bind(("127.0.0.1",port))
            break
        except:
            port += 1
    s.close()
    return port


my_port = bind_socket()

app = Flask(__name__)
app.secret_key = 'the random string'
app.config["SESSION_PERMANENT"] = True
@app.route('/nlp', methods=['POST'])
def process_input():
    input_text = None
    
    if 'text' not in request.form:
        return "ERROR"
    input_text = request.form['text'].split(" ")  # Filter out no alphabetical characters

    cmd = input_text[0]


    html = "<div class='responses'>"

    all_commands = [("/add", "Adds to playlist"),
                    ("/remove", "Removes from playlist"),
                    ("/list", "List playlist"),
                    ("/clear", "Clears playlist")]

    match cmd:
        case "/add":
            arguments = ''.join(input_text[1:])
            song_name = arguments.split("-")[0]
            artist_name = arguments.split("-")[1]
            response = playlist_add_song(session["user"], "default", song_name, artist_name)
            html += response
        case "/remove":
            arguments = ''.join(input_text[1:])
            song_name = arguments.split("-")[0]
            artist_name = arguments.split("-")[1]
            response = playlist_remove_song(session["user"], "default", song_name, artist_name)
            html += response
        case "/list":
            playlist = list_playlist(session["user"], "default")
            if playlist is not None:
                html += render_playlist(playlist)
        case "/clear":
            response = clear_playlist(session["user"], "default")
            html += response
        case "/help":
            html += "<ul>"
            for command, explanation in all_commands:
                html += f"<li>{command} - {explanation}"
            html += "</ul>"
        case _:
            html += "<p>Unknown command</p>"
    
    html+="</div>"
    return html


@app.route('/', methods=["GET"])
def index():
    session["user"] = "ove"
    new_user(session["user"], "ove")

    return render_template('index.html')

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=my_port,debug=False)
    serve(app, host='0.0.0.0', port=8000) # Production run
## To get auto reload use:
# flask --app main.py --debug run

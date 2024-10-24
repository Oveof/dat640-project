PORT_NUMBER = 8000
from datetime import timedelta
import string
import random
import sqlite3
import numpy as np

from waitress import serve
from flask import Flask, request, jsonify , render_template, session

from source.nlp import handle_nonempty_user_input
from source.db import create_user


app = Flask(__name__,
            static_folder='templates/assets',
            template_folder='templates'
            )
app.secret_key = 'the random string'
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=365)


@app.route('/', methods=["GET"])
def index():
    if "user" not in session:
        user_id = ''.join(random.choices(string.ascii_lowercase, k=64))
        session["user"] = user_id
        session.permanent = True
        create_user(user_id,'')

    return render_template('index.html')

@app.route('/components/chat', methods=["POST"])
def chat_submit():
    user_text = request.form['text']
    if user_text=="":
        return "",404

    response=handle_nonempty_user_input(user_text)
    return render_template("components/chat.html",user_text=user_text, response=response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT_NUMBER,debug=True)
    # serve(app,
    #       host='0.0.0.0',
    #       port=PORT_NUMBER) # Production run




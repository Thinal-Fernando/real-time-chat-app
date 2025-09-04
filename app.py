from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import random


app = Flask(__name__)
app.secret_key = "@123"

socketio = SocketIO(app, cors_allowed_origins="*")
active_users = {}

def genarate_guest_name():
    return f"Guest{random.randint(1000,9999)}"

@app.route("/")
def index():
    if "username" not in session:
        session["username"] = genarate_guest_name()
    return render_template('index.html', username = session["username"])


@socketio.event
def connect():
    print("A user connected")


@socketio.event
def disconnect():
    print("A user disconnected")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import random
from datetime import datetime


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


@socketio.event  #function bellow will listent for a socketIO event (connect)
def connect():
    username = session.get("username", genarate_guest_name())    # looks in the users flask session for username if not found creates one
    active_users[request.sid] = username    #storing unique id given by socket in thr dictionary
    emit("active_users", list(active_users.values()), broadcast=True)    #emit sends a event called active_users to all clients cause broadcast is true with a list of all active usernames
    emit("message", {"username": "System","msg": f"{username} joined the chat."}, broadcast=True)

@socketio.event
def disconnect():
    if request.sid in active_users:   # checking if ID exists in the dictionary
        del active_users[request.sid]    # removes the user from the active user list
        emit("active_users", list(active_users.values()), broadcast=True)   # updates all the clients again
        username = active_users[request.sid]
        emit("message", {"username": "System","msg": f"{username} joined the chat."}, broadcast=True)


@socketio.on("message")
def messages(data):
    message = data.get("msg", "")
    if message.strip():
        emit("message", {"username": session["username"], "msg": message, "timestamp": datetime.now().strftime("%H:%M:%S")}, broadcast=True)



if __name__ == "__main__":
    app.run(debug=True)

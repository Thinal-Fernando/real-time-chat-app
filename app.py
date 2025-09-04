from flask import Flask, render_template, request, session
from flask_socketio import SocketIO


app = Flask(__name__)
app.secret_key = "@123"

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from flask import copy_current_request_context

app = Flask(__name__)
app.secret_key = 'labai_slapta'
socketio = SocketIO(app)

# Kvietimo kodas ir vartotojai
INVITE_CODE = "Tarka123"
USERS = {
    "Majus": "Lohelis123",
    "Arūnas": "Zuokas123",
    "Kristupas": "Myžnius123",
}

# Prisijungimo puslapis
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        invite = request.form.get("invite")
        username = request.form.get("username")
        password = request.form.get("password")
        if invite == INVITE_CODE and username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect(url_for("chat"))
        else:
            return render_template("index.html", error="Neteisingi duomenys arba kvietimo kodas.")
    return render_template("index.html", error=None)

# Chat puslapis
@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("chat.html", username=session["username"])

# SocketIO žinučių siuntimas
@socketio.on("send_message")
def handle_send_message(data):
    @copy_current_request_context
    def process_message():
        username = session.get("username", "Nežinomas")
        message = data["message"]
        emit("receive_message", {"user": username, "message": message}, broadcast=True)
    process_message()

if __name__ == "__main__":
    socketio.run(app, debug=True)
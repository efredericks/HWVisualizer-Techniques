# https://medium.com/@swaroopkml96/deploying-your-p5-js-sketch-using-flask-on-heroku-8702492047f5
# https://gabrieltanner.org/blog/realtime-drawing-app/

## TBD
# - CORS issue when running on web server


####
# Class name must match filename
#   * provide constructor, update functions
#   * accept a palette and sketch information minimally
#   * tick rate?
#   * hook into firebase for saved images?
#      * i.e., create a unique entry per connection

from flask import Flask, render_template, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

import os,  json
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 's3cr3t'
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

currentState = {}

starttime = None
endtime = None
isDone = False

### Sockets

## STATUS WF:
# unittest sends socket message (status) for status to server.py
# server.py sends socket message (status) to sketch.js
# sketch.js sends socket message back (client_status) to server.py with isDone flag
# if isDone, return time, else return None

# @socketio.on("get_status")
# def handle_status(data):
#     socketio.emit('status', None)

# @socketio.on("client_status")
# def handle_client_status(data):
#     global starttime, endtime, isDone
#     isDone = data

#     print(data)

#     if data == "done":
#         print("Roundtrip time: {0}".format(endtime-starttime))
#     else:
#         print("Not done!")

# @socketio.on("status")
# def handle_status(data):
#     socketio.emit('status', None)

@socketio.on("done")
def handle_done(data):
    global starttime, isDone
    print("Client done.")
    endtime = datetime.datetime.now()
    print("Roundtrip time: {0}".format(endtime-starttime))
    socketio.emit("CLIENT_IS_DONE",None)
    isDone = True
    with open('./tests/client-done', 'a') as f:
        f.write("Roundtrip time: {0}".format(endtime-starttime))
        # .close()
    # socketio.stop()

@socketio.on("connected")
def handle_connection(data):
    global starttime
    global currentState
    print("User connected: {0}".format(data))

    starttime = datetime.datetime.now()



    if currentState != {}:
        socketio.emit('set initial data', {'bgColor': currentState})

### Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    socketio.run(app, port=8081)
    # app.run(debug=True)
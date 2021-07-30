from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import numpy as np
import base64
import sys
import cv2

# local imports
import static.run_model as run_model
application = Flask(__name__)
application.config['DEBUG'] = True
application.config['SECRET_KEY'] = "\xd9\xf9\xc6\xcd\x85\x0f\xa0\x92\x82\x1d\xce\x06\xa2\xddO\x1b0B\xbf\t6\x90s"

# if deploying to a server, make sure "threading" is set
socketio = SocketIO(application, logger=True, engineio_logger=True,
                    async_mode="threading")

model = run_model.get_model('static/saved_model')


@socketio.on('process frame', namespace='/')
def run_prediction(input):
    """Recieve URL encoded image, decode, run model prediction on the image, send results back to client.

    Parameters:
    -----------
        input (json): json packet from client, contains an encoded image
    """
    encoded_img = input.split(",")[1]
    try:
        nparr = np.frombuffer(base64.b64decode(encoded_img), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        prediction_dict = run_model_prediction(frame)
        emit('pred', prediction_dict)
    except Exception as e:
        print(f"\n{e}\n")
        print("couldn't decode images!", file=sys.stderr, flush=True)


@socketio.on('connect', namespace='/')
def test_connect():
    """Connect to clients and send welcome message."""
    print("client connected: ", file=sys.stderr, flush=True)
    emit('welcome', "Welcome to the server!")


@socketio.on('disconnect', namespace='/')
def test_disconnect():
    """Log when a client disconnects"""
    print("client disconnected: ", file=sys.stderr, flush=True)


@application.route('/')
def home_page():
    """Render home html page"""
    return render_template('home.html')


@application.route('/model_predictions')
def model_predictions():
    """Render model html page"""
    return render_template('model.html')


def run_model_prediction(frame):
    """Run prediction on a provided frame.

    Paramters:
    ----------
        frame (np.array): image captured from webcam
    
    Returns:
    --------
        predictions (dict): prediction dict containing string mapped values
    """
    try:
        img = run_model.process_image(frame, run_model.get_model_vars())
    except Exception as e:
        print(e)
        print("Couldn't process image", file=sys.stderr, flush=True)

    age, race, gender = model.predict(img)
    age, race, gender = run_model.process_results(age, race, gender, run_model.get_model_vars())

    predictions = {"Age": age, "Race": race, "Gender": gender}

    return predictions


if __name__ == "__main__":
    socketio.run(application)
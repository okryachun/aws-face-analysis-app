import logging
from flask import Flask, Response, render_template, request
from flask_socketio import SocketIO
import logging
import cv2
import sys
import numpy as np
import base64

# local imports
#import static.run_model as run_model

application = Flask(__name__)
application.config['DEBUG'] = True
application.logger.addHandler(logging.StreamHandler(sys.stdout))
socketio = SocketIO(application)

#model = run_model.get_model('static/saved_model')



#predict_img = False
#predictions = ""

# @socketio.on('input image', namespace='/test')
# def test_message(input):
#     print("just recieved an image!!!", file=sys.stderr, flush=True)
#     encoded_img = input.split(",")[1]
#     try:
#         nparr = np.fromstring(base64.b64decode(encoded_img), np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#         cv2.imshow("", img)
#         cv2.waitKey(3000)
#     except:
#         print("couln't decode images!", file=sys.stderr, flush=True)


@socketio.on('connect')
def test_connect():
    print("client connected: ", file=sys.stderr, flush=True)

@socketio.on('disconnect')
def test_disconnect():
    print("client disconnect...", file=sys.stderr, flush=True)


@application.route('/')
def home_page():
    """Render home html page"""
    print("This should 100% print", file=sys.stderr, flush=True)
    return render_template('home.html')


@application.route('/model_predictions', methods=['GET', 'POST'])
def model_predictions():
    """Listen for prediction requests, set global 'predict_img' to True when detected.

    Returns:
    --------
        render_template('model.html'): send model.html page
    """
    global predict_img

    if request.method == 'POST':
        if request.form.get('predict_button') == 'predict':
            predict_img = True

    elif request.method == 'GET':
        return render_template('model.html')
            
    return render_template('model.html')


# def run_model_prediction(frame):
#     """Run prediction on a provided frame.

#     Paramters:
#     ----------
#         frame (np.array): image captured from webcam
    
#     Returns:
#     --------
#         text (str): prediction string containing string mapped values
#     """
#     try:
#         img = run_model.process_image(frame, run_model.get_model_vars())
#     except:
#         print("Couldn't process image", file=sys.stderr, flush=True)

#     age, race, gender = model.predict(img)
#     age, race, gender = run_model.process_results(age, race, gender, run_model.get_model_vars())

#     text = f"Age: {age}, Race: {race}, Gender: {gender}"
#     print(text, file=sys.stderr, flush=True)

#     return text

if __name__ == "__main__":
    socketio.run(application)
import logging
from flask import Flask, Response, render_template, request
# from flask_socketio import SocketIO, emit
# import cv2
import sys
# import numpy as np
# import base64

# local imports
# import static.run_model as run_model

application = Flask(__name__)
application.config['DEBUG'] = True
application.config['SECRET_KEY'] = "\xd9\xf9\xc6\xcd\x85\x0f\xa0\x92\x82\x1d\xce\x06\xa2\xddO\x1b0B\xbf\t6\x90s"
# socketio = SocketIO(application)

# model = run_model.get_model('static/saved_model')

# @socketio.on('input image', namespace='/test')
# def run_prediction(input):
#     encoded_img = input.split(",")[1]
#     try:
#         nparr = np.frombuffer(base64.b64decode(encoded_img), np.uint8)
#         frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#         print(f"image was decoded! Here is the shape {frame.shape}")
#         # prediction_text = run_model_prediction(frame)
#         # print(f"{prediction_text}", file=sys.stderr, flush=True)
#     except Exception as e:
#         print(f"\n{e}\n")
#         print("couldn't decode images!", file=sys.stderr, flush=True)
    #emit("stats", {'prediction', 'complete'})


# @socketio.on('connect', namespace='/')
# def test_connect():
#     print("client connected: ", file=sys.stderr, flush=True)

# @socketio.on('message', namespace='/')
# def test_connect():
#     print("client connected: ", file=sys.stderr, flush=True)

@application.route('/')
def home_page():
    """Render home html page"""
    return render_template('home.html')


@application.route('/model_predictions')
def model_predictions():
    """Render model html page"""
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
    application.run()
    # socketio.run(application)
from flask import Flask, Response, app, render_template, request
#import cv2
import sys

# local imports
#import static.run_model as run_model
#from static.camera import VideoCamera

application = Flask(__name__)

#video_stream = VideoCamera()
#model = run_model.get_model('static/saved_model')

#predict_img = False
#predictions = ""

@application.route('/')
def home_page():
    """Render home html page"""
    return render_template('home.html')


# def gen(camera):
#     """Image frame generating function, loops continuously capturing and displaying images.

#         Other functions:
#             - Reads 'predict_img' variable, when true -> send frame for prediction -> reset 'predict_img'
#             - Display prediction results on cv2 frame
            
#     Parameters:
#     -----------
#         camera (cv2.VideoCapture): cv2 camera instance stream
#     Yield:
#     ------
#         jpeg_bytes (bytes): jpeg image converted to bytes and formatted as 'Content-Type: image/jpeg'
#     """
#     global predict_img, predictions

#     while True:
#         frame = camera.get_frame()
        
#         if predict_img:
#             predictions = run_model_prediction(frame)
#             predict_img = False

#         put_text = run_model.optimize_text(predictions, frame)
#         cv2.putText(**put_text)
#         _, jpeg = cv2.imencode('.jpg', frame)
#         jpeg_bytes = jpeg.tobytes()

#         yield (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + jpeg_bytes + b'\r\n\r\n')


# @application.route('/video_feed')
# def video_feed():
#     """Send Response of video generator stream"""
#     return Response(gen(video_stream),
#                 mimetype='multipart/x-mixed-replace; boundary=frame')


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
    application.debug = True
    application.run()
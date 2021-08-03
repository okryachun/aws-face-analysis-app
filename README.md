# Simple Web Application Deployment of [Tensorflow Face Analysis](https://github.com/okryachun/Tensorflow-Face-Analysis) via AWS Elastic Beanstalk Server

A Flask web application structured to deploy on an AWS Elastic Beanstalk Server.

This is a very simple application designed to easily showcase the trained neural network model trained [here](https://github.com/okryachun/Tensorflow-Face-Analysis). If you are interested in a more detailed description on how the convolutional neural network model works or was trained, visit the links above.

To run this web application go to this link: <https://facepredictions.com>

<br>

# Application Outline

Development Tools
- Backend is developed using Python with Flask framework
- Frontend is developed using JS/HTML/CSS
- Server hosted on AWS using Elastic Beanstalk

Application Flow
- Client sends an encoded image frame (from user's webcam) to server when "predict" button pressed
- Server receives encoded image, decodes image, runs model.predict on image, sends results to client
- Client receives image prediction results and displays them on screen

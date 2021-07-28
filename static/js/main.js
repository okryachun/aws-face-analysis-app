$(document).ready(function() {
    let namespace = "/test";
    let video = document.querySelector("#video-box");
    let canvas = document.querySelector("#canvas-box");
    let predict_button = document.querySelector("#model-button");
    let ctx = canvas.getContext('2d');

    var localMediaStream = null;

    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var socket = io.connect('http://127.0.0.1:5000');

    predict_button.addEventListener("click", function() {
        console.log("The predict button was pressed!");
        if (!localMediaStream) {
            return;
        }

        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

         let dataURL = canvas.toDataURL('image/jpeg');
         console.log(dataURL)
         //socket.emit('input image', dataURL);
    });

    socket.on('connect', function() {
        console.log('Connected!');
        // socket.send('ping', {foo:'bar'})
    });

    var constraints = {
        video: {
            width: { min: 640 },
            height: { min: 480 }
        }
    };


    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        video.srcObject = stream;
        localMediaStream = stream;
  
    }).catch(function(error) {
        console.log(error);
    });

});
  
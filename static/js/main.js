$(document).ready(function() {
    let video = document.querySelector("#video-box");
    let canvas = document.querySelector("#canvas-box");
    let predict_button = document.querySelector("#model-button");
    let ctx = canvas.getContext('2d');
    var localMediaStream = null;
    var socket = io();

    socket.on('connect', function() {
        console.log('Connected!');
    });

    // send frame to server for processing when predict button pressed
    predict_button.addEventListener("click", function() {
        if (!localMediaStream) {
            return;
        }
        if (canvas.height !== video.videoHeight) {
            canvas.height = video.videoHeight;
            canvas.width = video.videoWidth;
        }

        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

        let dataURL = canvas.toDataURL('image/jpeg');
        socket.emit('process frame', dataURL);
    });

    // display prediction results
    socket.on('pred', function(data) {
        $("#age").val(data["Age"]);
        $("#gender").val(data["Gender"]);
        $("#race").val(data["Race"]);
        console.log(data);
    });

    // acknowledge a welcome message from the server
    socket.on('welcome', function(data) {
        console.log(data)
    });

    var constraints = {
        video: {
            width: { min: 400 }, 
            height: { min: 300 }
        }
    };

    // open camera on browser
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        video.srcObject = stream;
        video.setAttribute("playsinline", true);
        localMediaStream = stream;
  
    }).catch(function(error) {
        console.log(error);
    });

});
  
$(document).ready(function() {
    let namespace = "/test";
    let video = document.querySelector("#video-box");
    let canvas = document.querySelector("#canvas-box");
    let predict_button = document.querySelector("#model-button");
    let ctx = canvas.getContext('2d');

    var localMediaStream = null;

    var socket = io();

    socket.on('connect', function() {
        console.log('Connected!');
    });

    socket.on('predictions', function(data) {
        $("#age").val(data["Age"]);
        $("#gender").val(data["Gender"]);
        $("#race").val(data["Race"])
        console.log(data);
    });


    predict_button.addEventListener("click", function() {
        if (!localMediaStream) {
            return;
        }

        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

        let dataURL = canvas.toDataURL('image/jpeg');
        socket.emit('frame capture', dataURL);
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
  
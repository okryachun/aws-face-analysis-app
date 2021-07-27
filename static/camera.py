import cv2

class VideoCamera():
    """Video camera streaming class"""
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        """Capture a frame from cv2 video stream. Loop until successfully captured.
        
        Returns:
        --------
            frame (np.array): capture image frame
        """
        # loop until ret returns True (i.e. successfully captured image)
        ret = False
        while True:
            ret, frame = self.video.read()
            if ret:
                break

        return  frame



#!/usr/bin/env python

#flask
from flask import Flask, render_template, Response

#OpenCV/ ROS 
import cv2
from cv_bridge import CvBridge, CvBridgeError

import rospy
from sensor_msgs.msg import Image

#Others
import numpy as np
import time
import datetime
import sys  

class video_process:
    def __init__(self):
        self.frame = 0

    """ROS callback func """
    def imageCallback(self, data): 
  
        try:
            bridge = CvBridge()
            cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
            ret, buffer = cv2.imencode('.jpg', cv_image)
            self.frame = buffer.tobytes()

        except CvBridgeError as e:
            rospy.logerr("cannot decode image")

        


stream = video_process()

"""node initialization"""

rospy.init_node("opencv_sub", anonymous=True )
rospy.Subscriber("camera/image", Image, stream.imageCallback, queue_size=5)


"""-------------------------------------------------------
web streaming start"""

app = Flask(__name__)

@app.route('/')  #site name 
def index():
    """Video streaming home page."""
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
            'title':'Image Streaming',
            'time': timeString
            }
    return render_template('index.html', **templateData)

 

def gen_frames():
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
       
        yield (b'--frame\r\n' 
                b'Content-Type: image/jpeg\r\n\r\n' + stream.frame + b'\r\n')

    cv2.destroyAllWindows()


       
"""--------------------------------------------------------------"""
 
@app.route('/video_feed')

def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

 

if __name__ == '__main__':
    app.run() #you can assign port num
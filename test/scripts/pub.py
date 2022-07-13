#!/usr/bin/env python

import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import rospy
from sensor_msgs.msg import Image
import cv2 

bridge = CvBridge()

def image_pub():
    
    cap = cv2.VideoCapture(0)
    rospy.init_node("opencv_pub", anonymous=True )
    pub = rospy.Publisher("camera/image", Image, queue_size=1)
    fps = cap.get(cv2.CAP_PROP_FPS)  
    rate = rospy.Rate(fps)

    while not rospy.is_shutdown():
        check, frame = cap.read()
        cv2.imshow("frame", frame)
      

        try:
            pub.publish(bridge.cv2_to_imgmsg(frame,"bgr8"))
        except CvBridgeError as err:
            print (err)

        cv2.waitKey(1)

        rate.sleep()

        

if __name__ == '__main__':
    try:
        image_pub()
    except rospy.ROSInterruptException:
        pass
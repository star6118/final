#!/usr/bin/env python


import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import rospy
from sensor_msgs.msg import Image



def imageCallback(data): 
  
  try:
    # frame = cv2.imdecode(data, 1)
    # cv2.imshow("view", frame)
    # cv2.waitKey(1)
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")

    cv2.imshow("view", cv_image)
    cv2.waitKey(1)
  

  except CvBridgeError as e:
    rospy.logerr("cannot decode image")
  
def image_sub(): 
  rospy.init_node("opencv_sub", anonymous=True )
  rospy.Subscriber("camera/image", Image, imageCallback, queue_size=5)
  rospy.spin()


if __name__ == '__main__':
  image_sub()
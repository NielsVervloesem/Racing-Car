#!/usr/bin/env python3
import rospy
from rospy_tutorials.msg import Floats
from sensor_msgs.msg import Joy
import time

def move_car(data):
    speed = data.data[0]
    angle = data.data[1]

    joystick.axes[0] = speed
    joystick.axes[1] = angle

    rospy.loginfo("MOVING CAR!")

    print("hm?")
    joy_pub.publish(joystick)

if __name__ == '__main__':
    rospy.init_node("Pilot_Node", anonymous=False)
    rospy.Subscriber("/prediction", Floats, move_car)

    joy_pub = rospy.Publisher('/joy', Joy, queue_size=1)

    joystick = Joy(axes=[0.0,0.0])

    rospy.loginfo("SPINNING PILOT NODE!")
    rospy.spin()
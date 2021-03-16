#!/usr/bin/env python3
import rospy
import time
from sensor_msgs.msg import Range
from rospy_tutorials.msg import Floats
from random import randrange

def read(data, number):
    if(number == 2):
        sensor_data[2] = data.range

    if(number == 3):
        sensor_data[3] = data.range

    if(number == 4):
        sensor_data[4] = data.range

    if(number == 5):
        sensor_data[5] = data.range

    if(number == 6):
        sensor_data[6] = data.range

    sensor_publisher.publish(sensor_data)

if __name__ == '__main__':
    rospy.init_node("sensor_node", anonymous=False)

    sensor_publisher = rospy.Publisher('/sensors', Floats, queue_size=1)

    #maybe aparte callback voor iedere functie
    #welke range is welke hoek?
    rospy.Subscriber('/range_3', Range, read, 2)
    rospy.Subscriber('/range_4', Range, read, 3)
    rospy.Subscriber('/range_5', Range, read, 4)
    rospy.Subscriber('/range_6', Range, read, 5)
    rospy.Subscriber('/range_7', Range, read, 6)

    sensor_data = [0,0,0,0,0,0,0,0]
    sensor_publisher.publish(sensor_data)

    rospy.loginfo("SPINNING SENSOR NODE!")
    rospy.spin()


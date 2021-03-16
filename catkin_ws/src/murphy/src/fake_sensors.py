#!/usr/bin/env python


import rospy
from rospy_tutorials.msg import Floats
from random import randrange

def talker():
    sensor_publisher = rospy.Publisher('/sensors', Floats, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        mes = [randrange(120),randrange(120),randrange(120),randrange(120),randrange(120),randrange(120),randrange(120),randrange(120)]
        sensor_publisher.publish(mes)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
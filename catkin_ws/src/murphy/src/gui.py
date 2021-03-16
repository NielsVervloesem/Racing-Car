#!/usr/bin/env python

import rospy
import sys

from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import Joy
from std_msgs.msg import String

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from std_msgs.msg import Bool


GUI_UPDATE_PERIOD = 0.10 

class GUI(QWidget):
    def __init__(self):
        super(GUI, self).__init__()
        #rospy.Subscriber('/range_7', Range, self._range_cb , queue_size=1)
        self.sensor_subscriber = rospy.Subscriber("/sensors", Floats, self.update_sensor)
        self.bla = rospy.Subscriber("/chatter", String, self.hm)

        self.prediction_subscriber = rospy.Subscriber("/prediction", Floats, self.update_prediction)
        self.joy_subscriber = rospy.Subscriber("/joy", Joy, self.update_joy)

        self.pub_ai = rospy.Publisher('/ai', Bool, queue_size=1)
        self.isActivated = False


        self.init_ui()

    def init_ui(self):
        self.mainWindow = QWidget()

        self.sensorLabel = QLabel(self)
        self.sensorLabel.move(10,10)
        self.sensorLabel.resize(400,10)        

        self.predictionLabel = QLabel(self)
        self.predictionLabel.move(10,50)
        self.predictionLabel.resize(400,10)

        self.joyLabel = QLabel(self)
        self.joyLabel.move(10,90)
        self.joyLabel.resize(400,15)

        button1 = QPushButton(self)
        button1.setText("Activate AI")
        button1.move(10,130)
        button1.clicked.connect(self.activate_AI)

        self.setGeometry(100, 100, 760, 410)
        self.setWindowTitle('Murphy Dashboard')
        self.show()

    def hm(self, data):
        self.sensorLabel.setText("Sensor data " + str(data.data))


    def update_sensor(self, data):
        self.sensorLabel.setText("Sensor data " + str(data.data))

    def update_prediction(self, data):
        self.predictionLabel.setText("Prediction data " + str(data.data))

    def update_joy(self, data):
        self.joyLabel.setText("Joy data angle+speed " + str(data.axes[0]) + " " + str(data.axes[1])) 

    def activate_AI(self):
        if(not self.isActivated):
            self.isActivated = True
        else:
            self.isActivated = False

        self.pub_ai.publish(self.isActivated)

if __name__ == '__main__':
    rospy.init_node("gui_node")
    application = QApplication(sys.argv)
    gui = GUI()

    sys.exit(application.exec_())
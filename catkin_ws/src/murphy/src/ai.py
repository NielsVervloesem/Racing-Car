#!/usr/bin/env python3
import pickle
import neat

import os
import rospy
import random
from rospy_tutorials.msg import Floats

def process_data(data):

    print(data.data)
    #Clean data for model, normalize or other stuff
    output = winner_model.activate(data.data)
    rospy.loginfo(output)

    output = [random.uniform(0.0, 1.0),random.uniform(-1.0, 1.0)]

    prediction_pub.publish(output)

if __name__ == '__main__':
    rospy.init_node("neat_node", anonymous=False)
    
    cwd = os.getcwd()


    model_path = cwd + '/model/model.pkl'
    config_file = cwd +'/model/config.txt'

    with open(model_path, "rb") as f:
        winner = pickle.load(f)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_file)

    winner_model = neat.nn.FeedForwardNetwork.create(winner, config)

    prediction_pub = rospy.Publisher('/prediction', Floats, queue_size=1)
    subscriber = rospy.Subscriber('/sensors', Floats, process_data)

    rospy.loginfo("SPINNING NEAT NODE!")
    rospy.spin()
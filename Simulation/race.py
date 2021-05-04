import pickle
import neat
import pygame
from racetrack import Racetrack
from randomtrack import RandomRacetrack

from car import Car
import random
import sys
import time
import math
import os
from neat.math_util import softmax
import numpy as np
import visualize

#Pygame init
background_colour = (0,0,0)
(width, height) = (800, 800)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Murphy simulation')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

screen.fill(background_colour)
pygame.display.flip()
clock = pygame.time.Clock()

racetrack = RandomRacetrack(width, height, 15)
car_x = int(racetrack.start[0])
car_y = int(racetrack.start[1])

#red, green, blue, yellow, cyan, pink
colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255), (255,0,255),(255,0,255),(255,0,255),(255,0,255),(255,0,255),(255,0,255)]
modelName = []

networks = []
cars = []

for filename in os.listdir("Models"):
    if(filename.endswith("pkl")):
        filename = filename[:-4]
        model_path = "Models/" + filename + ".pkl"
        config_file = "Models/" + filename + ".txt"

        with open(model_path, "rb") as f:
            winner = pickle.load(f)

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

        winner_model = neat.nn.FeedForwardNetwork.create(winner, config)

        networks.append(winner_model)
        cars.append(Car(filename, car_x, car_y, 80))
        modelName.append(filename)
        nodes = {0:'Speed',1:'Angle'}
        #visualize.draw_net(config, winner, True,node_names=nodes, filename=filename)

dt = 0.17
run = True
for i in range(100):
    run = True
    remain = 6
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        #Draw racetrack
        for line in racetrack.innerHitLine:
            pygame.draw.lines(screen, (255,0,0), False, line,2)

        for line in racetrack.outerHitLine:
            pygame.draw.lines(screen, (255,0,0), False, line,2)

        colorOffset = 0
        for i in range(0,len(racetrack.checkpoints),2):
            p1 = (int(racetrack.checkpoints[i][0]),int(racetrack.checkpoints[i][1]))
            p2 = (int(racetrack.checkpoints[i+1][0]),int(racetrack.checkpoints[i+1][1]))
            pygame.draw.line(screen, (0, 255 - colorOffset,0+colorOffset), p1, p2, 1)    
            colorOffset = colorOffset + 5

        #Loop cars and make them drive
        for index, car in enumerate(cars):
            if(car.is_alive):
                #180, -90, -40, -15, 0, 15, 40, 90
                sensors = car.radar.calculate_distance(racetrack)
                output = networks[index].activate(sensors)

                if(len(output) > 2):
                    softmax_result = softmax(output)
                    class_output = np.argmax(((softmax_result / np.max(softmax_result)) == 1).astype(int))
                    
                    if(class_output == 0):
                        car.velocity[0] = car.velocity[0] + 1
                        car.steering = 0

                    if(class_output == 1):
                        car.velocity[0] = car.velocity[0] - 1
                        car.steering = 0

                    if(class_output == 2):
                        if(car.steering < 45):
                            car.steering = car.steering + 5

                    if(class_output == 3):
                        if(car.steering > -45):
                            car.steering = car.steering - 5

                    if(class_output == 4):
                        if(car.steering < 45):
                            car.steering = car.steering + 15

                    if(class_output == 5):
                        if(car.steering > -45):
                            car.steering = car.steering - 15

                    if(class_output == 6):
                        if(car.steering < 45):
                            car.steering = car.steering + 45

                    if(class_output == 7):
                        if(car.steering > -45):
                            car.steering = car.steering - 45
                else:
                    car.velocity[0] = output[0] * 20
                    car.steering = output[1] * 90 - 45
                car.update(dt)

                #Kill off bad cars
                if (racetrack.hit(car)):
                    car.is_alive = False
                    remain = remain - 1

                if remain == 0:
                    run = False

                #car.check_passed(racetrack)
                if(car.checkpoint_passed == len(racetrack.checkpoints)):
                    car.is_alive = False
                    run = False
                
                #Draw each cars (no radar lines because of lag)
                
                for line in car.radar.radar_lines:
                    pygame.draw.line(screen, (0,0,255), line[0], line[1], 1)
                
                
                pygame.draw.circle(screen, colors[index], (int(car.position.x), int(car.position.y)), car.length)

                jump = 0
                i = 0
                for name in modelName:
                    textsurface = myfont.render((name), False, colors[i])
                    screen.blit(textsurface,(0,jump))
                    jump = jump + 20
                    i = i + 1
                        #update screen
        pygame.display.update()
        screen.fill(background_colour)
        clock.tick(60)

    racetrack = RandomRacetrack(width, height, 15)
    car_x = int(racetrack.start[0])
    car_y = int(racetrack.start[1])

    #red, green, blue, yellow, cyan, pink
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255)]
    modelName = []

    networks = []
    cars = []

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


model_path = "ackermanV1.pkl"
config_file = "config-feedforward.txt"


with open(model_path, "rb") as f:
    winner = pickle.load(f)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)

winner_model = neat.nn.FeedForwardNetwork.create(winner, config)

car_x = 400
car_y = 400
car_length = 50
car_width = 30 
wheel_length = 10 
wheel_width = 5

p1 = [car_x-car_length/2,car_y-car_width/2]
p2 = [car_x+(0.5*car_length),car_y-car_width/2]
p3 = [car_x+(0.5*car_length),car_y+car_width/2]
p4 = [car_x-car_length/2,car_y+car_width/2]

angles = [180, -90, -40, -15, 0, 15, 40, 90]
maxLenght = 130
sensors = [maxLenght,maxLenght,maxLenght,maxLenght,maxLenght,maxLenght,maxLenght,maxLenght]
inputdata = [1,1,1,1,1,1,1,1]
run = True

while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_q]:
        if(sensors[0] < maxLenght):
            sensors[0] += 1
    if pressed[pygame.K_a]:
        if(sensors[0] > 0):
            sensors[0] -= 1
   
    if pressed[pygame.K_w]:
        if(sensors[1] < maxLenght):
            sensors[1] += 1
    if pressed[pygame.K_s]:
        if(sensors[1] > 0):
            sensors[1] -= 1

    if pressed[pygame.K_e]:
        if(sensors[2] < maxLenght):
            sensors[2] += 1
    if pressed[pygame.K_d]:
        if(sensors[2] > 0):
            sensors[2] -= 1

    if pressed[pygame.K_r]:
        if(sensors[3] < maxLenght):
            sensors[3] += 1
    if pressed[pygame.K_f]:
        if(sensors[3] > 0):
            sensors[3] -= 1

    if pressed[pygame.K_t]:
        if(sensors[4] < maxLenght):
            sensors[4] += 1
    if pressed[pygame.K_g]:
        if(sensors[4] > 0):
            sensors[4] -= 1

    if pressed[pygame.K_y]:
        if(sensors[5] < maxLenght):
            sensors[5] += 1
    if pressed[pygame.K_h]:
        if(sensors[5] > 0):
            sensors[5] -= 1

    if pressed[pygame.K_u]:
        if(sensors[6] < maxLenght):
            sensors[6] += 1
    if pressed[pygame.K_j]:
        if(sensors[6] > 0):
            sensors[6] -= 1

    if pressed[pygame.K_i]:
        if(sensors[7] < maxLenght):
            sensors[7] += 1
    if pressed[pygame.K_k]:
        if(sensors[7] > 0):
            sensors[7] -= 1

    pygame.draw.polygon(screen, (255,0,0), (p1,p2,p3,p4))

    for i in range(len(sensors)):
        endpoint = (int(car_x + math.cos(math.radians(angles[i])) * sensors[i]),int(car_y + math.sin(math.radians(angles[i])) * sensors[i]))
        pygame.draw.circle(screen, (255,255,2), endpoint, 2)
        textsurface = myfont.render(str(sensors[i]), False, (255, 255, 255))
        screen.blit(textsurface,(endpoint))
        inputdata[i] =  sensors[i] / maxLenght


    output = winner_model.activate(inputdata)
    angle = output[1] * 40 * 2 - 40
    angle = -angle

    endpoint = (int(car_x + math.cos(math.radians(angle)) * 200),int(car_y + math.sin(math.radians(angle)) * 200))
    pygame.draw.line(screen, (0,255,0), (400,400), endpoint,1)

    textsurface = myfont.render(str(round(angle,2)), False, (255, 255, 255))
    screen.blit(textsurface,((400,400)))
    pygame.display.update()
    screen.fill(background_colour)
    clock.tick(60)


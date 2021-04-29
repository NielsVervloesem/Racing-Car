import pygame
import os
from racetrack import Racetrack
from randomtrack import RandomRacetrack
from car import Car
from math import sin, radians, degrees, copysign
import time
import datetime
import neat
import sys
import pickle
import random
import numpy as np
from neat.math_util import softmax
from random import randrange

#MODEL PARAMS INIT
name = "ModelV26"
config_path = "./config-feedforward.txt"
carMaxSpeed = 20 * 1
carSensors = 8
drawRacetrack = True
racetrack_file = 'modelsV3\\racketrackV1.pkl'


        
#Pygame init
(width, height) = (1000, 1000)
background_colour = (0,0,0)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Murphy simulation')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
screen.fill(background_colour)
pygame.display.flip()
clock = pygame.time.Clock()
racetrack = RandomRacetrack(width, height, 30)

#Draw racetrack
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        racetrack = RandomRacetrack(width, height, 30)
        time.sleep(0.2)
        
    for line in racetrack.innerHitLine:
        pygame.draw.lines(screen, (255,0,0), False, line,2)

    for line in racetrack.outerHitLine:
        pygame.draw.lines(screen, (255,0,0), False, line,2)

    colorOffset = 0
    p1 = (int(racetrack.checkpoints[0][0]),int(racetrack.checkpoints[0][1]))
    p2 = (int(racetrack.checkpoints[1][0]),int(racetrack.checkpoints[1][1]))
    pygame.draw.line(screen, (255,0,0), p1, p2, 2)    

    for i in range(2,len(racetrack.checkpoints)-2,2):
        p1 = (int(racetrack.checkpoints[i][0]),int(racetrack.checkpoints[i][1]))
        p2 = (int(racetrack.checkpoints[i+1][0]),int(racetrack.checkpoints[i+1][1]))
        pygame.draw.line(screen, (0, 255 - colorOffset,0+colorOffset), p1, p2, 1)    
        colorOffset = colorOffset + 5

    p1 = (int(racetrack.checkpoints[len(racetrack.checkpoints)-2][0]),int(racetrack.checkpoints[len(racetrack.checkpoints)-2][1]))
    p2 = (int(racetrack.checkpoints[len(racetrack.checkpoints)-1][0]),int(racetrack.checkpoints[len(racetrack.checkpoints)-1][1]))
    pygame.draw.line(screen, (255,255,255), p1, p2, 3)  

    #update screen
    pygame.display.update()
    screen.fill(background_colour)
    clock.tick(60)

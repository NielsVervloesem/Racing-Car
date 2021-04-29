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

car_x = int(racetrack.start[0])
car_y = int(racetrack.start[1])

car = Car(8, car_x, car_y, 60, racetrack.startAngle)

dt = 0.17
run = True
while run:
    #Draw racetrack
    for line in racetrack.innerHitLine:
        pygame.draw.lines(screen, (255,0,0), False, line)

    for line in racetrack.outerHitLine:
        pygame.draw.lines(screen, (255,0,0), False, line)
    
    colorOffset = 0
    for i in range(0,len(racetrack.checkpoints),2):
        p1 = (int(racetrack.checkpoints[i][0]),int(racetrack.checkpoints[i][1]))
        p2 = (int(racetrack.checkpoints[i+1][0]),int(racetrack.checkpoints[i+1][1]))
        pygame.draw.line(screen, (0, 255 - colorOffset,0+colorOffset), p1, p2, 1)    
        colorOffset = colorOffset + 5
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.exit = True

    # User input
    pressed = pygame.key.get_pressed()
    sensors = car.radar.calculate_distance(racetrack) 
    if pressed[pygame.K_UP]:
        if car.velocity.x < 0:
            car.acceleration = car.brake_deceleration
        else:
            car.acceleration += 1 * dt
        
    elif pressed[pygame.K_DOWN]:
        if car.velocity.x > 0:
            car.acceleration = -car.brake_deceleration
        else:
            car.acceleration -= 1 * dt
    elif pressed[pygame.K_SPACE]:
        if abs(car.velocity.x) > dt * car.brake_deceleration:
            car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
        else:
            car.acceleration = -car.velocity.x / dt
    else:
        if abs(car.velocity.x) > dt * car.free_deceleration:
            car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
        else:
            if dt != 0:
                car.acceleration = -car.velocity.x / dt

    if pressed[pygame.K_RIGHT]:
        car.steering -= 30 * dt
    elif pressed[pygame.K_LEFT]:
        car.steering += 30 * dt
    else:
        car.steering = 0
    if(car.velocity[0] > 5):
        car.velocity[0] = 5
    car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

    # Logic
    car.update2(dt)
    car.check_passed(racetrack)
    print(racetrack.hit(car))
    pygame.draw.circle(screen, (255,0,0), (int(car.position.x), int(car.position.y)), car.length)

    #update screen
    pygame.display.update()
    screen.fill(background_colour)
    clock.tick(60)

